"""
Assertion Management Module for PyTestSuite Pro

This module provides advanced assertion strategies including hard assertions,
soft assertions, and warning assertions for comprehensive test validation.
"""

import logging
import traceback
from typing import Any, List, Dict, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import pytest


class AssertionLevel(Enum):
    """Assertion severity levels"""
    HARD = "HARD"      # Critical - test fails immediately
    SOFT = "SOFT"      # Collected - test fails at end if any soft assertions fail
    WARNING = "WARNING" # Non-critical - logged but doesn't fail test


@dataclass
class AssertionResult:
    """Result of an assertion operation"""
    level: AssertionLevel
    passed: bool
    message: str
    expected: Any = None
    actual: Any = None
    exception: Optional[Exception] = None
    traceback_info: Optional[str] = None


@dataclass
class AssertionSummary:
    """Summary of all assertions in a test"""
    total: int = 0
    passed: int = 0
    failed: int = 0
    warnings: int = 0
    hard_failures: List[AssertionResult] = field(default_factory=list)
    soft_failures: List[AssertionResult] = field(default_factory=list)
    warning_failures: List[AssertionResult] = field(default_factory=list)


class AssertionManager:
    """Manages different types of assertions and their results"""
    
    def __init__(self):
        self.results: List[AssertionResult] = []
        self.logger = self._setup_logger()
        self._test_context = None
        
    def _setup_logger(self) -> logging.Logger:
        """Set up logging for assertions"""
        logger = logging.getLogger('AssertionManager')
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger
    
    def reset(self):
        """Reset assertion results for new test"""
        self.results.clear()
        self._test_context = None
    
    def set_test_context(self, test_name: str):
        """Set current test context for better reporting"""
        self._test_context = test_name
        self.logger.debug(f"Set test context: {test_name}")
    
    def hard_assert(self, condition: bool, message: str, expected: Any = None, actual: Any = None):
        """
        Hard assertion - fails immediately if condition is False
        Use for critical functionality that must work
        """
        result = AssertionResult(
            level=AssertionLevel.HARD,
            passed=condition,
            message=message,
            expected=expected,
            actual=actual
        )
        
        self.results.append(result)
        
        if condition:
            self.logger.info(f"✓ HARD ASSERT PASSED: {message}")
        else:
            error_msg = self._format_error_message(result)
            self.logger.error(f"✗ HARD ASSERT FAILED: {error_msg}")
            pytest.fail(error_msg)
    
    def soft_assert(self, condition: bool, message: str, expected: Any = None, actual: Any = None):
        """
        Soft assertion - collects failures but doesn't stop test execution
        Use for UI validations or multiple related checks
        """
        result = AssertionResult(
            level=AssertionLevel.SOFT,
            passed=condition,
            message=message,
            expected=expected,
            actual=actual
        )
        
        if not condition:
            result.traceback_info = traceback.format_stack()
        
        self.results.append(result)
        
        if condition:
            self.logger.info(f"✓ SOFT ASSERT PASSED: {message}")
        else:
            error_msg = self._format_error_message(result)
            self.logger.warning(f"✗ SOFT ASSERT FAILED: {error_msg}")
    
    def warning_assert(self, condition: bool, message: str, expected: Any = None, actual: Any = None):
        """
        Warning assertion - logs failure but doesn't affect test result
        Use for performance checks or non-critical features
        """
        result = AssertionResult(
            level=AssertionLevel.WARNING,
            passed=condition,
            message=message,
            expected=expected,
            actual=actual
        )
        
        self.results.append(result)
        
        if condition:
            self.logger.info(f"✓ WARNING ASSERT PASSED: {message}")
        else:
            error_msg = self._format_error_message(result)
            self.logger.warning(f"⚠ WARNING ASSERT FAILED: {error_msg}")
    
    def assert_equals(self, actual: Any, expected: Any, message: str = None, level: AssertionLevel = AssertionLevel.HARD):
        """Assert that two values are equal"""
        if message is None:
            message = f"Expected {expected}, but got {actual}"
        
        condition = actual == expected
        
        if level == AssertionLevel.HARD:
            self.hard_assert(condition, message, expected, actual)
        elif level == AssertionLevel.SOFT:
            self.soft_assert(condition, message, expected, actual)
        else:
            self.warning_assert(condition, message, expected, actual)
    
    def assert_not_equals(self, actual: Any, expected: Any, message: str = None, level: AssertionLevel = AssertionLevel.HARD):
        """Assert that two values are not equal"""
        if message is None:
            message = f"Expected {actual} to not equal {expected}"
        
        condition = actual != expected
        
        if level == AssertionLevel.HARD:
            self.hard_assert(condition, message, f"!= {expected}", actual)
        elif level == AssertionLevel.SOFT:
            self.soft_assert(condition, message, f"!= {expected}", actual)
        else:
            self.warning_assert(condition, message, f"!= {expected}", actual)
    
    def assert_contains(self, container: Any, item: Any, message: str = None, level: AssertionLevel = AssertionLevel.HARD):
        """Assert that container contains item"""
        if message is None:
            message = f"Expected {container} to contain {item}"
        
        try:
            condition = item in container
        except TypeError:
            condition = False
        
        if level == AssertionLevel.HARD:
            self.hard_assert(condition, message, f"contains {item}", container)
        elif level == AssertionLevel.SOFT:
            self.soft_assert(condition, message, f"contains {item}", container)
        else:
            self.warning_assert(condition, message, f"contains {item}", container)
    
    def assert_true(self, condition: bool, message: str = None, level: AssertionLevel = AssertionLevel.HARD):
        """Assert that condition is True"""
        if message is None:
            message = f"Expected condition to be True, but was {condition}"
        
        if level == AssertionLevel.HARD:
            self.hard_assert(condition, message, True, condition)
        elif level == AssertionLevel.SOFT:
            self.soft_assert(condition, message, True, condition)
        else:
            self.warning_assert(condition, message, True, condition)
    
    def assert_false(self, condition: bool, message: str = None, level: AssertionLevel = AssertionLevel.HARD):
        """Assert that condition is False"""
        if message is None:
            message = f"Expected condition to be False, but was {condition}"
        
        is_false = not condition
        
        if level == AssertionLevel.HARD:
            self.hard_assert(is_false, message, False, condition)
        elif level == AssertionLevel.SOFT:
            self.soft_assert(is_false, message, False, condition)
        else:
            self.warning_assert(is_false, message, False, condition)
    
    def assert_greater_than(self, actual: Any, expected: Any, message: str = None, level: AssertionLevel = AssertionLevel.HARD):
        """Assert that actual is greater than expected"""
        if message is None:
            message = f"Expected {actual} to be greater than {expected}"
        
        condition = actual > expected
        
        if level == AssertionLevel.HARD:
            self.hard_assert(condition, message, f"> {expected}", actual)
        elif level == AssertionLevel.SOFT:
            self.soft_assert(condition, message, f"> {expected}", actual)
        else:
            self.warning_assert(condition, message, f"> {expected}", actual)
    
    def assert_less_than(self, actual: Any, expected: Any, message: str = None, level: AssertionLevel = AssertionLevel.HARD):
        """Assert that actual is less than expected"""
        if message is None:
            message = f"Expected {actual} to be less than {expected}"
        
        condition = actual < expected
        
        if level == AssertionLevel.HARD:
            self.hard_assert(condition, message, f"< {expected}", actual)
        elif level == AssertionLevel.SOFT:
            self.soft_assert(condition, message, f"< {expected}", actual)
        else:
            self.warning_assert(condition, message, f"< {expected}", actual)
    
    def assert_length(self, container: Any, expected_length: int, message: str = None, level: AssertionLevel = AssertionLevel.HARD):
        """Assert that container has expected length"""
        try:
            actual_length = len(container)
            if message is None:
                message = f"Expected length {expected_length}, but got {actual_length}"
            
            condition = actual_length == expected_length
            
            if level == AssertionLevel.HARD:
                self.hard_assert(condition, message, expected_length, actual_length)
            elif level == AssertionLevel.SOFT:
                self.soft_assert(condition, message, expected_length, actual_length)
            else:
                self.warning_assert(condition, message, expected_length, actual_length)
                
        except TypeError as e:
            error_msg = f"Object {container} has no length: {str(e)}"
            if level == AssertionLevel.HARD:
                self.hard_assert(False, error_msg)
            elif level == AssertionLevel.SOFT:
                self.soft_assert(False, error_msg)
            else:
                self.warning_assert(False, error_msg)
    
    def _format_error_message(self, result: AssertionResult) -> str:
        """Format detailed error message for assertion failure"""
        msg = result.message
        
        if result.expected is not None and result.actual is not None:
            msg += f"\n  Expected: {result.expected}"
            msg += f"\n  Actual:   {result.actual}"
        
        if self._test_context:
            msg = f"[{self._test_context}] {msg}"
        
        return msg
    
    def get_summary(self) -> AssertionSummary:
        """Get summary of all assertion results"""
        summary = AssertionSummary()
        
        for result in self.results:
            summary.total += 1
            
            if result.passed:
                summary.passed += 1
            else:
                summary.failed += 1
                
                if result.level == AssertionLevel.HARD:
                    summary.hard_failures.append(result)
                elif result.level == AssertionLevel.SOFT:
                    summary.soft_failures.append(result)
                else:  # WARNING
                    summary.warnings += 1
                    summary.warning_failures.append(result)
        
        return summary
    
    def finalize_assertions(self):
        """
        Finalize assertions for test completion
        Called at end of test to handle soft assertion failures
        """
        summary = self.get_summary()
        
        # Log summary
        self.logger.info(f"Assertion Summary - Total: {summary.total}, "
                        f"Passed: {summary.passed}, Failed: {summary.failed}, "
                        f"Warnings: {summary.warnings}")
        
        # Handle soft assertion failures
        if summary.soft_failures:
            failure_messages = []
            for failure in summary.soft_failures:
                failure_messages.append(self._format_error_message(failure))
            
            error_msg = f"Test had {len(summary.soft_failures)} soft assertion failure(s):\n" + \
                       "\n".join([f"  - {msg}" for msg in failure_messages])
            
            self.logger.error(error_msg)
            pytest.fail(error_msg)


# Global assertion manager instance
assertion_manager = AssertionManager()


# Convenience functions for easy access
def hard_assert(condition: bool, message: str, expected: Any = None, actual: Any = None):
    """Hard assertion convenience function"""
    assertion_manager.hard_assert(condition, message, expected, actual)


def soft_assert(condition: bool, message: str, expected: Any = None, actual: Any = None):
    """Soft assertion convenience function"""
    assertion_manager.soft_assert(condition, message, expected, actual)


def warning_assert(condition: bool, message: str, expected: Any = None, actual: Any = None):
    """Warning assertion convenience function"""
    assertion_manager.warning_assert(condition, message, expected, actual)


# Pytest fixture for assertion management
@pytest.fixture
def assertions():
    """Pytest fixture that provides assertion manager and handles cleanup"""
    import inspect
    
    # Get test name from the calling frame
    frame = inspect.currentframe()
    test_name = "unknown_test"
    try:
        for frame_info in inspect.stack():
            if frame_info.function.startswith('test_'):
                test_name = frame_info.function
                break
    except:
        pass
    finally:
        del frame
    
    # Reset and set context
    assertion_manager.reset()
    assertion_manager.set_test_context(test_name)
    
    yield assertion_manager
    
    # Finalize assertions after test completion
    try:
        assertion_manager.finalize_assertions()
    except Exception as e:
        # If finalize fails, at least log the summary
        summary = assertion_manager.get_summary()
        logging.error(f"Failed to finalize assertions: {e}")
        logging.info(f"Final summary: {summary.total} total, "
                    f"{summary.passed} passed, {summary.failed} failed")
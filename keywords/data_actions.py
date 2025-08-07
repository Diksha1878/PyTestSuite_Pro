"""
Data Actions Keywords for PyTestSuite Pro

This module provides keywords for handling test data from various sources
including JSON, CSV, YAML files and databases.
"""

import os
import json
import csv
import yaml
import logging
from typing import Dict, List, Any, Optional, Union
import pandas as pd
from faker import Faker


class DataActions:
    """Data management keywords for test automation"""
    
    def __init__(self):
        self.logger = self._setup_logger()
        self.faker = Faker()
        self.test_data_dir = "test_data"
        self.cached_data: Dict[str, Any] = {}
    
    def _setup_logger(self) -> logging.Logger:
        """Set up logging for data actions"""
        logger = logging.getLogger('DataActions')
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger
    
    # File Loading Keywords
    def load_json_data(self, filename: str, cache_key: str = None) -> Dict[str, Any]:
        """
        Load data from JSON file
        
        Args:
            filename: JSON filename (relative to test_data directory)
            cache_key: Optional cache key to store data
            
        Returns:
            Dict: JSON data
        """
        file_path = os.path.join(self.test_data_dir, "json", filename)
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"JSON file not found: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if cache_key:
                self.cached_data[cache_key] = data
            
            self.logger.info(f"JSON data loaded from: {filename}")
            return data
            
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse JSON file {filename}: {str(e)}")
            raise
    
    def load_csv_data(self, filename: str, cache_key: str = None) -> List[Dict[str, str]]:
        """
        Load data from CSV file
        
        Args:
            filename: CSV filename (relative to test_data directory)
            cache_key: Optional cache key to store data
            
        Returns:
            List[Dict]: CSV data as list of dictionaries
        """
        file_path = os.path.join(self.test_data_dir, "csv", filename)
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"CSV file not found: {file_path}")
        
        try:
            data = []
            with open(file_path, 'r', encoding='utf-8') as f:
                csv_reader = csv.DictReader(f)
                data = list(csv_reader)
            
            if cache_key:
                self.cached_data[cache_key] = data
            
            self.logger.info(f"CSV data loaded from: {filename} ({len(data)} rows)")
            return data
            
        except Exception as e:
            self.logger.error(f"Failed to load CSV file {filename}: {str(e)}")
            raise
    
    def load_yaml_data(self, filename: str, cache_key: str = None) -> Dict[str, Any]:
        """
        Load data from YAML file
        
        Args:
            filename: YAML filename (relative to test_data directory)
            cache_key: Optional cache key to store data
            
        Returns:
            Dict: YAML data
        """
        file_path = os.path.join(self.test_data_dir, "yaml", filename)
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"YAML file not found: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            if cache_key:
                self.cached_data[cache_key] = data
            
            self.logger.info(f"YAML data loaded from: {filename}")
            return data
            
        except yaml.YAMLError as e:
            self.logger.error(f"Failed to parse YAML file {filename}: {str(e)}")
            raise
    
    def load_excel_data(self, filename: str, sheet_name: str = None, cache_key: str = None) -> List[Dict[str, Any]]:
        """
        Load data from Excel file
        
        Args:
            filename: Excel filename (relative to test_data directory)
            sheet_name: Sheet name to load (first sheet if None)
            cache_key: Optional cache key to store data
            
        Returns:
            List[Dict]: Excel data as list of dictionaries
        """
        file_path = os.path.join(self.test_data_dir, filename)
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Excel file not found: {file_path}")
        
        try:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            data = df.to_dict('records')
            
            if cache_key:
                self.cached_data[cache_key] = data
            
            sheet_info = f" (sheet: {sheet_name})" if sheet_name else ""
            self.logger.info(f"Excel data loaded from: {filename}{sheet_info} ({len(data)} rows)")
            return data
            
        except Exception as e:
            self.logger.error(f"Failed to load Excel file {filename}: {str(e)}")
            raise
    
    # Cache Management Keywords
    def get_cached_data(self, cache_key: str) -> Any:
        """
        Get data from cache
        
        Args:
            cache_key: Cache key
            
        Returns:
            Any: Cached data
        """
        if cache_key not in self.cached_data:
            raise KeyError(f"No cached data found for key: {cache_key}")
        
        return self.cached_data[cache_key]
    
    def cache_data(self, cache_key: str, data: Any):
        """
        Cache data with specific key
        
        Args:
            cache_key: Key to store data under
            data: Data to cache
        """
        self.cached_data[cache_key] = data
        self.logger.info(f"Data cached with key: {cache_key}")
    
    def clear_cache(self, cache_key: str = None):
        """
        Clear cached data
        
        Args:
            cache_key: Specific key to clear (clears all if None)
        """
        if cache_key:
            if cache_key in self.cached_data:
                del self.cached_data[cache_key]
                self.logger.info(f"Cleared cached data for key: {cache_key}")
        else:
            self.cached_data.clear()
            self.logger.info("Cleared all cached data")
    
    # Data Generation Keywords
    def generate_user_data(self, count: int = 1) -> Union[Dict[str, str], List[Dict[str, str]]]:
        """
        Generate fake user data
        
        Args:
            count: Number of user records to generate
            
        Returns:
            Dict or List[Dict]: Generated user data
        """
        def create_user():
            return {
                'first_name': self.faker.first_name(),
                'last_name': self.faker.last_name(),
                'email': self.faker.email(),
                'username': self.faker.user_name(),
                'password': self.faker.password(length=12),
                'phone': self.faker.phone_number(),
                'address': self.faker.address(),
                'city': self.faker.city(),
                'country': self.faker.country(),
                'postal_code': self.faker.postcode(),
                'date_of_birth': self.faker.date_of_birth().strftime('%Y-%m-%d'),
                'company': self.faker.company(),
                'job_title': self.faker.job(),
                'ssn': self.faker.ssn()
            }
        
        if count == 1:
            user_data = create_user()
            self.logger.info("Generated single user data")
            return user_data
        else:
            users_data = [create_user() for _ in range(count)]
            self.logger.info(f"Generated {count} user records")
            return users_data
    
    def generate_product_data(self, count: int = 1) -> Union[Dict[str, str], List[Dict[str, str]]]:
        """
        Generate fake product data
        
        Args:
            count: Number of product records to generate
            
        Returns:
            Dict or List[Dict]: Generated product data
        """
        def create_product():
            return {
                'name': self.faker.catch_phrase(),
                'description': self.faker.text(max_nb_chars=200),
                'price': str(self.faker.pydecimal(left_digits=3, right_digits=2, positive=True)),
                'category': self.faker.word(),
                'sku': self.faker.ean13(),
                'brand': self.faker.company(),
                'color': self.faker.color_name(),
                'weight': str(self.faker.pyfloat(left_digits=2, right_digits=2, positive=True)),
                'dimensions': f"{self.faker.pyfloat(1, 2, True)}x{self.faker.pyfloat(1, 2, True)}x{self.faker.pyfloat(1, 2, True)}",
                'in_stock': str(self.faker.boolean()),
                'quantity': str(self.faker.random_int(min=0, max=100))
            }
        
        if count == 1:
            product_data = create_product()
            self.logger.info("Generated single product data")
            return product_data
        else:
            products_data = [create_product() for _ in range(count)]
            self.logger.info(f"Generated {count} product records")
            return products_data
    
    def generate_random_string(self, length: int = 10, include_numbers: bool = True, 
                              include_special: bool = False) -> str:
        """
        Generate random string
        
        Args:
            length: String length
            include_numbers: Include numbers in string
            include_special: Include special characters
            
        Returns:
            str: Random string
        """
        import string
        import random
        
        chars = string.ascii_letters
        if include_numbers:
            chars += string.digits
        if include_special:
            chars += "!@#$%^&*"
        
        random_string = ''.join(random.choice(chars) for _ in range(length))
        self.logger.info(f"Generated random string of length {length}")
        return random_string
    
    def generate_random_email(self, domain: str = None) -> str:
        """
        Generate random email address
        
        Args:
            domain: Email domain (uses faker default if None)
            
        Returns:
            str: Random email address
        """
        if domain:
            local_part = self.faker.user_name()
            email = f"{local_part}@{domain}"
        else:
            email = self.faker.email()
        
        self.logger.info(f"Generated random email: {email}")
        return email
    
    # Data Manipulation Keywords
    def filter_data(self, data: List[Dict], filter_key: str, filter_value: Any) -> List[Dict]:
        """
        Filter list of dictionaries by key-value pair
        
        Args:
            data: List of dictionaries to filter
            filter_key: Key to filter by
            filter_value: Value to match
            
        Returns:
            List[Dict]: Filtered data
        """
        filtered_data = [item for item in data if item.get(filter_key) == filter_value]
        self.logger.info(f"Filtered data: {len(filtered_data)} items match {filter_key}={filter_value}")
        return filtered_data
    
    def get_data_by_index(self, data: List, index: int) -> Any:
        """
        Get data item by index
        
        Args:
            data: List of data items
            index: Index to retrieve
            
        Returns:
            Any: Data item at index
        """
        if index >= len(data):
            raise IndexError(f"Index {index} out of range for data with {len(data)} items")
        
        item = data[index]
        self.logger.info(f"Retrieved data item at index {index}")
        return item
    
    def get_random_data_item(self, data: List) -> Any:
        """
        Get random item from data list
        
        Args:
            data: List of data items
            
        Returns:
            Any: Random data item
        """
        import random
        
        if not data:
            raise ValueError("Cannot get random item from empty data list")
        
        item = random.choice(data)
        self.logger.info("Retrieved random data item")
        return item
    
    def merge_data(self, *data_sources: Dict) -> Dict:
        """
        Merge multiple data dictionaries
        
        Args:
            *data_sources: Data dictionaries to merge
            
        Returns:
            Dict: Merged data dictionary
        """
        merged_data = {}
        
        for data in data_sources:
            if isinstance(data, dict):
                merged_data.update(data)
        
        self.logger.info(f"Merged {len(data_sources)} data sources")
        return merged_data
    
    # Data Validation Keywords
    def validate_data_structure(self, data: Dict, required_keys: List[str]) -> bool:
        """
        Validate that data contains required keys
        
        Args:
            data: Data dictionary to validate
            required_keys: List of required keys
            
        Returns:
            bool: True if all required keys present
        """
        missing_keys = [key for key in required_keys if key not in data]
        
        if missing_keys:
            self.logger.error(f"Missing required keys: {missing_keys}")
            return False
        
        self.logger.info("Data structure validation passed")
        return True
    
    def validate_email_format(self, email: str) -> bool:
        """
        Validate email format
        
        Args:
            email: Email address to validate
            
        Returns:
            bool: True if email format is valid
        """
        import re
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        is_valid = bool(re.match(email_pattern, email))
        
        self.logger.info(f"Email format validation for '{email}': {is_valid}")
        return is_valid
    
    # Data Saving Keywords
    def save_data_to_json(self, data: Dict, filename: str):
        """
        Save data to JSON file
        
        Args:
            data: Data to save
            filename: JSON filename (relative to test_data directory)
        """
        file_path = os.path.join(self.test_data_dir, "json", filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Data saved to JSON file: {filename}")
            
        except Exception as e:
            self.logger.error(f"Failed to save JSON file {filename}: {str(e)}")
            raise
    
    def save_data_to_csv(self, data: List[Dict], filename: str):
        """
        Save data to CSV file
        
        Args:
            data: List of dictionaries to save
            filename: CSV filename (relative to test_data directory)
        """
        if not data:
            raise ValueError("Cannot save empty data to CSV")
        
        file_path = os.path.join(self.test_data_dir, "csv", filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        try:
            fieldnames = data[0].keys()
            
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            
            self.logger.info(f"Data saved to CSV file: {filename} ({len(data)} rows)")
            
        except Exception as e:
            self.logger.error(f"Failed to save CSV file {filename}: {str(e)}")
            raise
    
    def append_data_to_csv(self, data: Dict, filename: str):
        """
        Append single data record to existing CSV file
        
        Args:
            data: Data dictionary to append
            filename: CSV filename (relative to test_data directory)
        """
        file_path = os.path.join(self.test_data_dir, "csv", filename)
        
        file_exists = os.path.exists(file_path)
        
        try:
            with open(file_path, 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=data.keys())
                
                if not file_exists:
                    writer.writeheader()
                
                writer.writerow(data)
            
            self.logger.info(f"Data appended to CSV file: {filename}")
            
        except Exception as e:
            self.logger.error(f"Failed to append to CSV file {filename}: {str(e)}")
            raise
    
    # Environment-based Data Keywords
    def get_environment_data(self, key: str, default: Any = None) -> Any:
        """
        Get data specific to current environment
        
        Args:
            key: Data key
            default: Default value if key not found
            
        Returns:
            Any: Environment-specific data
        """
        from config import env_manager
        
        env_name = env_manager.current_env
        env_data_file = f"environment_{env_name}.json"
        
        try:
            env_data = self.load_json_data(env_data_file, cache_key=f"env_{env_name}")
            value = env_data.get(key, default)
            self.logger.info(f"Retrieved environment data for '{key}': {value}")
            return value
            
        except FileNotFoundError:
            self.logger.warning(f"Environment data file not found: {env_data_file}")
            return default
    
    def set_environment_data(self, key: str, value: Any):
        """
        Set data for current environment
        
        Args:
            key: Data key
            value: Data value
        """
        from config import env_manager
        
        env_name = env_manager.current_env
        env_data_file = f"environment_{env_name}.json"
        
        try:
            # Load existing data or create new
            try:
                env_data = self.load_json_data(env_data_file)
            except FileNotFoundError:
                env_data = {}
            
            # Update data
            env_data[key] = value
            
            # Save back to file
            self.save_data_to_json(env_data, env_data_file)
            
            # Update cache
            self.cache_data(f"env_{env_name}", env_data)
            
            self.logger.info(f"Set environment data '{key}': {value}")
            
        except Exception as e:
            self.logger.error(f"Failed to set environment data: {str(e)}")
            raise
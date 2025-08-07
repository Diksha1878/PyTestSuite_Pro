pipeline {
    agent {
        label 'test-automation'
    }
    
    parameters {
        choice(
            name: 'TEST_SUITE',
            choices: ['smoke', 'regression', 'api', 'ui', 'integration', 'performance', 'security', 'all'],
            description: 'Select test suite to execute'
        )
        choice(
            name: 'ENVIRONMENT',
            choices: ['dev', 'staging', 'prod'],
            description: 'Target environment for testing'
        )
        choice(
            name: 'BROWSER',
            choices: ['chrome', 'firefox', 'edge', 'all'],
            description: 'Browser for UI tests'
        )
        booleanParam(
            name: 'PARALLEL_EXECUTION',
            defaultValue: true,
            description: 'Enable parallel test execution'
        )
        booleanParam(
            name: 'HEADLESS',
            defaultValue: true,
            description: 'Run UI tests in headless mode'
        )
        string(
            name: 'CUSTOM_MARKERS',
            defaultValue: '',
            description: 'Custom pytest markers (optional)'
        )
    }
    
    environment {
        PYTHON_VERSION = '3.9'
        TEST_ENV = "${params.ENVIRONMENT}"
        BROWSER = "${params.BROWSER}"
        HEADLESS = "${params.HEADLESS}"
        PARALLEL = "${params.PARALLEL_EXECUTION}"
        
        // Credentials
        API_TOKEN = credentials('api-token')
        DB_PASSWORD = credentials('database-password')
        
        // Selenium Grid
        SELENIUM_REMOTE_URL = credentials('selenium-grid-url')
        
        // Paths
        WORKSPACE_PATH = "${WORKSPACE}"
        REPORTS_PATH = "${WORKSPACE}/reports"
        LOGS_PATH = "${WORKSPACE}/logs"
    }
    
    options {
        buildDiscarder(logRotator(numToKeepStr: '30'))
        timeout(time: 2, unit: 'HOURS')
        timestamps()
        ansiColor('xterm')
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo "🔄 Checking out source code..."
                checkout scm
                
                script {
                    env.BUILD_TIMESTAMP = sh(
                        script: "date '+%Y%m%d_%H%M%S'",
                        returnStdout: true
                    ).trim()
                }
            }
        }
        
        stage('Environment Setup') {
            steps {
                echo "🏗️ Setting up test environment..."
                
                // Create directories
                sh """
                    mkdir -p ${REPORTS_PATH}
                    mkdir -p ${LOGS_PATH}
                    mkdir -p reports/screenshots
                    mkdir -p reports/page_sources
                """
                
                // Install Python dependencies
                sh """
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                """
                
                // Validate environment
                sh """
                    python --version
                    pip list
                    pytest --version
                """
            }
        }
        
        stage('Pre-test Validation') {
            steps {
                echo "✅ Running pre-test validations..."
                
                script {
                    // Validate test environment connectivity
                    try {
                        sh """
                            python -c "
from config import get_current_config
config = get_current_config()
print(f'Base URL: {config.base_url}')
print(f'API URL: {config.api_base_url}')
print(f'Environment: {config.name}')
                            "
                        """
                    } catch (Exception e) {
                        error("Environment configuration validation failed: ${e.getMessage()}")
                    }
                    
                    // Check Selenium Grid connectivity (if remote)
                    if (env.SELENIUM_REMOTE_URL) {
                        sh """
                            curl -f ${env.SELENIUM_REMOTE_URL}/status || echo "Warning: Selenium Grid not accessible"
                        """
                    }
                }
            }
        }
        
        stage('Test Execution') {
            parallel {
                stage('Smoke Tests') {
                    when {
                        anyOf {
                            equals expected: 'smoke', actual: params.TEST_SUITE
                            equals expected: 'all', actual: params.TEST_SUITE
                        }
                    }
                    steps {
                        echo "🚀 Running smoke tests..."
                        
                        script {
                            def parallelFlag = params.PARALLEL_EXECUTION ? '-n auto' : ''
                            def customMarkers = params.CUSTOM_MARKERS ? "and ${params.CUSTOM_MARKERS}" : ''
                            
                            sh """
                                pytest -m 'smoke ${customMarkers}' ${parallelFlag} \\
                                    --html=${REPORTS_PATH}/smoke-report.html \\
                                    --self-contained-html \\
                                    --junitxml=${REPORTS_PATH}/smoke-junit.xml \\
                                    --tb=short \\
                                    -v
                            """
                        }
                    }
                    post {
                        always {
                            publishHTML([
                                allowMissing: false,
                                alwaysLinkToLastBuild: true,
                                keepAll: true,
                                reportDir: 'reports',
                                reportFiles: 'smoke-report.html',
                                reportName: 'Smoke Test Report',
                                reportTitles: ''
                            ])
                        }
                    }
                }
                
                stage('API Tests') {
                    when {
                        anyOf {
                            equals expected: 'api', actual: params.TEST_SUITE
                            equals expected: 'regression', actual: params.TEST_SUITE
                            equals expected: 'all', actual: params.TEST_SUITE
                        }
                    }
                    steps {
                        echo "🔌 Running API tests..."
                        
                        script {
                            def parallelFlag = params.PARALLEL_EXECUTION ? '-n auto' : ''
                            def customMarkers = params.CUSTOM_MARKERS ? "and ${params.CUSTOM_MARKERS}" : ''
                            
                            sh """
                                pytest tests/api/ -m 'api ${customMarkers}' ${parallelFlag} \\
                                    --html=${REPORTS_PATH}/api-report.html \\
                                    --self-contained-html \\
                                    --junitxml=${REPORTS_PATH}/api-junit.xml \\
                                    --tb=short \\
                                    -v
                            """
                        }
                    }
                    post {
                        always {
                            publishHTML([
                                allowMissing: false,
                                alwaysLinkToLastBuild: true,
                                keepAll: true,
                                reportDir: 'reports',
                                reportFiles: 'api-report.html',
                                reportName: 'API Test Report',
                                reportTitles: ''
                            ])
                        }
                    }
                }
                
                stage('UI Tests') {
                    when {
                        anyOf {
                            equals expected: 'ui', actual: params.TEST_SUITE
                            equals expected: 'regression', actual: params.TEST_SUITE
                            equals expected: 'all', actual: params.TEST_SUITE
                        }
                    }
                    steps {
                        echo "🖥️ Running UI tests..."
                        
                        script {
                            def browsers = params.BROWSER == 'all' ? ['chrome', 'firefox', 'edge'] : [params.BROWSER]
                            def parallelFlag = params.PARALLEL_EXECUTION ? '-n auto' : ''
                            def customMarkers = params.CUSTOM_MARKERS ? "and ${params.CUSTOM_MARKERS}" : ''
                            
                            browsers.each { browser ->
                                echo "Testing with browser: ${browser}"
                                
                                sh """
                                    pytest tests/ui/ -m 'ui ${customMarkers}' ${parallelFlag} \\
                                        --browser=${browser} \\
                                        --html=${REPORTS_PATH}/ui-${browser}-report.html \\
                                        --self-contained-html \\
                                        --junitxml=${REPORTS_PATH}/ui-${browser}-junit.xml \\
                                        --tb=short \\
                                        -v
                                """
                            }
                        }
                    }
                    post {
                        always {
                            publishHTML([
                                allowMissing: false,
                                alwaysLinkToLastBuild: true,
                                keepAll: true,
                                reportDir: 'reports',
                                reportFiles: 'ui-*-report.html',
                                reportName: 'UI Test Reports',
                                reportTitles: ''
                            ])
                        }
                    }
                }
                
                stage('Integration Tests') {
                    when {
                        anyOf {
                            equals expected: 'integration', actual: params.TEST_SUITE
                            equals expected: 'regression', actual: params.TEST_SUITE
                            equals expected: 'all', actual: params.TEST_SUITE
                        }
                    }
                    steps {
                        echo "🔗 Running integration tests..."
                        
                        script {
                            def parallelFlag = params.PARALLEL_EXECUTION ? '-n auto' : ''
                            def customMarkers = params.CUSTOM_MARKERS ? "and ${params.CUSTOM_MARKERS}" : ''
                            
                            sh """
                                pytest tests/integration/ -m 'integration ${customMarkers}' ${parallelFlag} \\
                                    --html=${REPORTS_PATH}/integration-report.html \\
                                    --self-contained-html \\
                                    --junitxml=${REPORTS_PATH}/integration-junit.xml \\
                                    --tb=short \\
                                    -v
                            """
                        }
                    }
                    post {
                        always {
                            publishHTML([
                                allowMissing: false,
                                alwaysLinkToLastBuild: true,
                                keepAll: true,
                                reportDir: 'reports',
                                reportFiles: 'integration-report.html',
                                reportName: 'Integration Test Report',
                                reportTitles: ''
                            ])
                        }
                    }
                }
            }
        }
        
        stage('Performance Tests') {
            when {
                anyOf {
                    equals expected: 'performance', actual: params.TEST_SUITE
                    equals expected: 'all', actual: params.TEST_SUITE
                }
            }
            steps {
                echo "⚡ Running performance tests..."
                
                script {
                    def customMarkers = params.CUSTOM_MARKERS ? "and ${params.CUSTOM_MARKERS}" : ''
                    
                    sh """
                        pytest -m 'performance ${customMarkers}' \\
                            --html=${REPORTS_PATH}/performance-report.html \\
                            --self-contained-html \\
                            --junitxml=${REPORTS_PATH}/performance-junit.xml \\
                            --tb=short \\
                            -v
                    """
                }
            }
            post {
                always {
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'reports',
                        reportFiles: 'performance-report.html',
                        reportName: 'Performance Test Report',
                        reportTitles: ''
                    ])
                }
            }
        }
        
        stage('Security Tests') {
            when {
                anyOf {
                    equals expected: 'security', actual: params.TEST_SUITE
                    equals expected: 'all', actual: params.TEST_SUITE
                }
            }
            steps {
                echo "🔒 Running security tests..."
                
                script {
                    def customMarkers = params.CUSTOM_MARKERS ? "and ${params.CUSTOM_MARKERS}" : ''
                    
                    sh """
                        pytest -m 'security ${customMarkers}' \\
                            --html=${REPORTS_PATH}/security-report.html \\
                            --self-contained-html \\
                            --junitxml=${REPORTS_PATH}/security-junit.xml \\
                            --tb=short \\
                            -v
                    """
                }
            }
            post {
                always {
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'reports',
                        reportFiles: 'security-report.html',
                        reportName: 'Security Test Report',
                        reportTitles: ''
                    ])
                }
            }
        }
    }
    
    post {
        always {
            echo "📋 Post-execution steps..."
            
            // Collect test results
            publishTestResults testResultsPattern: 'reports/*-junit.xml'
            
            // Archive artifacts
            archiveArtifacts artifacts: 'reports/**/*', allowEmptyArchive: true
            archiveArtifacts artifacts: 'logs/**/*', allowEmptyArchive: true
            
            // Generate test summary
            script {
                def testSummary = """
                    Test Execution Summary:
                    - Suite: ${params.TEST_SUITE}
                    - Environment: ${params.ENVIRONMENT}
                    - Browser: ${params.BROWSER}
                    - Parallel: ${params.PARALLEL_EXECUTION}
                    - Build: ${env.BUILD_NUMBER}
                    - Timestamp: ${env.BUILD_TIMESTAMP}
                """.stripIndent()
                
                writeFile file: 'test-summary.txt', text: testSummary
                archiveArtifacts artifacts: 'test-summary.txt'
            }
        }
        
        success {
            echo "✅ Test execution completed successfully!"
            
            // Send success notification
            script {
                if (params.TEST_SUITE in ['regression', 'all']) {
                    emailext (
                        subject: "✅ Test Suite '${params.TEST_SUITE}' Passed - Build #${env.BUILD_NUMBER}",
                        body: """
                            The test suite '${params.TEST_SUITE}' has completed successfully.
                            
                            Environment: ${params.ENVIRONMENT}
                            Browser: ${params.BROWSER}
                            Build: ${env.BUILD_NUMBER}
                            
                            View reports: ${env.BUILD_URL}
                        """,
                        to: "${env.CHANGE_AUTHOR_EMAIL ?: 'team@example.com'}"
                    )
                }
            }
        }
        
        failure {
            echo "❌ Test execution failed!"
            
            // Send failure notification
            emailext (
                subject: "❌ Test Suite '${params.TEST_SUITE}' Failed - Build #${env.BUILD_NUMBER}",
                body: """
                    The test suite '${params.TEST_SUITE}' has failed.
                    
                    Environment: ${params.ENVIRONMENT}
                    Browser: ${params.BROWSER}
                    Build: ${env.BUILD_NUMBER}
                    
                    View reports and logs: ${env.BUILD_URL}
                    
                    Please investigate and fix the failing tests.
                """,
                to: "${env.CHANGE_AUTHOR_EMAIL ?: 'team@example.com'}"
            )
        }
        
        unstable {
            echo "⚠️ Test execution completed with warnings!"
        }
        
        cleanup {
            echo "🧹 Cleaning up..."
            
            // Clean up large files to save space
            sh """
                find . -name "*.log" -size +10M -delete
                find reports/screenshots -name "*.png" -mtime +7 -delete
            """
            
            // Clean up driver processes (if any)
            sh """
                pkill -f "chromedriver\\|geckodriver\\|msedgedriver" || true
            """
        }
    }
}
===================
Cloud Integration
===================

The Cloud Integration system provides unified authentication and session management for multiple cloud providers, enabling seamless integration with Azure and AWS services through the dtPyAppFramework.

Overview
========

dtPyAppFramework's cloud integration system abstracts authentication complexity and provides a consistent interface for accessing cloud services across different providers. The system supports:

* **Multi-Cloud Session Management**: Centralized authentication for multiple cloud providers
* **Credential Management**: Secure handling of cloud credentials and authentication tokens
* **Service Integration**: Seamless integration with secrets management and other framework components
* **Configuration-Driven**: Cloud sessions defined through application configuration
* **Environment Flexibility**: Support for different authentication methods based on deployment environment

Core Components
===============

CloudSessionManager
-------------------

The ``CloudSessionManager`` class provides centralized management of all cloud authentication sessions.

.. autoclass:: dtPyAppFramework.cloud.CloudSessionManager
   :members:
   :inherited-members:

Key Features:

**Singleton Pattern**
  Single instance manages all cloud sessions across the application lifecycle.

**Configuration-Based Setup**
  Cloud sessions are defined in application configuration files and automatically loaded.

**Session Lifecycle Management**
  Handles authentication, token refresh, and session cleanup automatically.

Cloud Session Types
====================

AWS Cloud Sessions
------------------

**AWSCloudSession**

.. autoclass:: dtPyAppFramework.cloud.aws.AWSCloudSession
   :members:

**Authentication Methods:**

* **AWS CLI Profiles**: Uses configured AWS CLI profiles
* **Environment Variables**: ``AWS_ACCESS_KEY_ID``, ``AWS_SECRET_ACCESS_KEY``, ``AWS_SESSION_TOKEN``
* **IAM Roles**: EC2 instance profiles and assumed roles
* **STS Temporary Credentials**: Short-lived credentials for enhanced security

**Configuration Example:**

.. code-block:: yaml

    cloud_sessions:
      - name: "aws_production"
        session_type: "aws"
        region: "us-east-1"
        profile: "production"        # AWS CLI profile name
        
      - name: "aws_development"
        session_type: "aws"
        region: "us-west-2"
        access_key_id: "ENV/AWS_ACCESS_KEY_ID"
        secret_access_key: "ENV/AWS_SECRET_ACCESS_KEY"
        
      - name: "aws_assumed_role"
        session_type: "aws"
        region: "eu-west-1"
        role_arn: "arn:aws:iam::123456789012:role/MyRole"
        session_name: "dtPyAppFramework-session"

Azure Cloud Sessions
--------------------

**AzureCloudSession**

.. autoclass:: dtPyAppFramework.cloud.azure.AzureCloudSession
   :members:

**Authentication Methods:**

* **DefaultAzureCredential**: Automatically tries multiple authentication methods
* **Service Principal**: Client ID and secret-based authentication
* **Managed Identity**: For Azure-hosted applications
* **Azure CLI**: Uses Azure CLI authentication token
* **Interactive Browser**: For development scenarios

**Configuration Example:**

.. code-block:: yaml

    cloud_sessions:
      - name: "azure_production"
        session_type: "azure"
        subscription_id: "ENV/AZURE_SUBSCRIPTION_ID"
        tenant_id: "ENV/AZURE_TENANT_ID"
        # Uses DefaultAzureCredential for authentication
        
      - name: "azure_service_principal"
        session_type: "azure"
        subscription_id: "12345678-1234-1234-1234-123456789012"
        tenant_id: "87654321-4321-4321-4321-210987654321"
        client_id: "ENV/AZURE_CLIENT_ID"
        client_secret: "SEC/azure_client_secret"
        
      - name: "azure_managed_identity"
        session_type: "azure"
        subscription_id: "ENV/AZURE_SUBSCRIPTION_ID"
        use_managed_identity: true

Configuration Integration
=========================

Session Configuration
---------------------

Cloud sessions are configured through the application's configuration system:

.. code-block:: yaml

    # config.yaml
    cloud_sessions:
      # AWS Sessions
      - name: "aws_primary"
        session_type: "aws"
        region: "us-east-1"
        profile: "default"
        
      - name: "aws_backup"
        session_type: "aws"  
        region: "us-west-2"
        access_key_id: "ENV/AWS_BACKUP_KEY_ID"
        secret_access_key: "SEC/aws_backup_secret"
        
      # Azure Sessions
      - name: "azure_primary"
        session_type: "azure"
        subscription_id: "ENV/AZURE_SUBSCRIPTION_ID"
        tenant_id: "ENV/AZURE_TENANT_ID"
        
      - name: "azure_keyvault"
        session_type: "azure"
        subscription_id: "ENV/AZURE_SUBSCRIPTION_ID"
        client_id: "ENV/AZURE_CLIENT_ID"
        client_secret: "SEC/azure_client_secret"

Secrets Manager Integration
---------------------------

Cloud sessions integrate seamlessly with the secrets management system:

.. code-block:: yaml

    # Link cloud sessions to secret stores
    secrets_manager:
      cloud_stores:
        aws_secrets:
          store_type: "aws"
          priority: 100
          region: "us-east-1"
          session_name: "aws_primary"      # References cloud session
          
        azure_keyvault:
          store_type: "azure"
          priority: 200
          vault_url: "https://myvault.vault.azure.net/"
          session_name: "azure_keyvault"   # References cloud session

Usage Examples
==============

Basic Session Access
--------------------

.. code-block:: python

    from dtPyAppFramework.cloud import CloudSessionManager

    # Get the cloud session manager
    cloud_manager = CloudSessionManager()

    # Get specific cloud sessions
    aws_session = cloud_manager.get_session("aws_primary")
    azure_session = cloud_manager.get_session("azure_primary")

    if aws_session:
        # Use AWS session for service calls
        s3_client = aws_session.client('s3')
        dynamodb = aws_session.resource('dynamodb')

    if azure_session:
        # Use Azure session for service calls
        from azure.keyvault.secrets import SecretClient
        secret_client = SecretClient(
            vault_url="https://myvault.vault.azure.net/",
            credential=azure_session
        )

AWS Service Integration
-----------------------

.. code-block:: python

    from dtPyAppFramework.cloud import CloudSessionManager
    import logging

    def upload_to_s3(file_path, bucket_name, object_key):
        """Upload file to S3 using configured session."""
        logger = logging.getLogger(__name__)
        cloud_manager = CloudSessionManager()
        
        # Get AWS session
        aws_session = cloud_manager.get_session("aws_primary")
        if not aws_session:
            raise ValueError("AWS session 'aws_primary' not configured")
        
        try:
            # Create S3 client
            s3_client = aws_session.client('s3')
            
            # Upload file
            s3_client.upload_file(file_path, bucket_name, object_key)
            logger.info(f"Uploaded {file_path} to s3://{bucket_name}/{object_key}")
            
        except Exception as ex:
            logger.error(f"Failed to upload to S3: {ex}")
            raise

    def read_from_dynamodb(table_name, key):
        """Read item from DynamoDB using configured session."""
        cloud_manager = CloudSessionManager()
        aws_session = cloud_manager.get_session("aws_primary")
        
        if not aws_session:
            raise ValueError("AWS session not configured")
        
        # Create DynamoDB resource
        dynamodb = aws_session.resource('dynamodb')
        table = dynamodb.Table(table_name)
        
        response = table.get_item(Key=key)
        return response.get('Item')

Azure Service Integration
-------------------------

.. code-block:: python

    from dtPyAppFramework.cloud import CloudSessionManager
    from azure.storage.blob import BlobServiceClient
    from azure.cosmos import CosmosClient
    import logging

    def upload_to_blob_storage(file_path, container_name, blob_name):
        """Upload file to Azure Blob Storage."""
        logger = logging.getLogger(__name__)
        cloud_manager = CloudSessionManager()
        
        # Get Azure session
        azure_session = cloud_manager.get_session("azure_primary")
        if not azure_session:
            raise ValueError("Azure session 'azure_primary' not configured")
        
        try:
            # Create blob service client
            blob_client = BlobServiceClient(
                account_url="https://myaccount.blob.core.windows.net",
                credential=azure_session
            )
            
            # Upload file
            with open(file_path, "rb") as data:
                blob_client.get_blob_client(
                    container=container_name, 
                    blob=blob_name
                ).upload_blob(data, overwrite=True)
                
            logger.info(f"Uploaded {file_path} to blob storage: {container_name}/{blob_name}")
            
        except Exception as ex:
            logger.error(f"Failed to upload to blob storage: {ex}")
            raise

    def query_cosmos_db(database_name, container_name, query):
        """Query Azure Cosmos DB using configured session."""
        cloud_manager = CloudSessionManager()
        azure_session = cloud_manager.get_session("azure_primary")
        
        if not azure_session:
            raise ValueError("Azure session not configured")
        
        # Create Cosmos client
        cosmos_client = CosmosClient(
            url="https://myaccount.documents.azure.com:443/",
            credential=azure_session
        )
        
        database = cosmos_client.get_database_client(database_name)
        container = database.get_container_client(container_name)
        
        items = list(container.query_items(query, enable_cross_partition_query=True))
        return items

Advanced Authentication Patterns
=================================

Role-Based Authentication
-------------------------

.. code-block:: python

    from dtPyAppFramework.cloud import CloudSessionManager
    from dtPyAppFramework.settings import Settings

    def get_environment_appropriate_session():
        """Get cloud session based on deployment environment."""
        settings = Settings()
        environment = settings.get('deployment.environment', 'development')
        
        cloud_manager = CloudSessionManager()
        
        if environment == 'production':
            # Use production session with assumed roles
            return cloud_manager.get_session("aws_production_role")
        elif environment == 'staging':
            # Use staging session
            return cloud_manager.get_session("aws_staging")
        else:
            # Use development session
            return cloud_manager.get_session("aws_development")

Multi-Region Support
--------------------

.. code-block:: yaml

    # Multi-region AWS configuration
    cloud_sessions:
      - name: "aws_us_east_1"
        session_type: "aws"
        region: "us-east-1"
        profile: "production"
        
      - name: "aws_eu_west_1" 
        session_type: "aws"
        region: "eu-west-1"
        profile: "production"
        
      - name: "aws_ap_southeast_1"
        session_type: "aws"
        region: "ap-southeast-1"
        profile: "production"

.. code-block:: python

    def multi_region_deployment(data, regions=['us-east-1', 'eu-west-1']):
        """Deploy data to multiple AWS regions."""
        cloud_manager = CloudSessionManager()
        
        for region in regions:
            session_name = f"aws_{region.replace('-', '_')}"
            session = cloud_manager.get_session(session_name)
            
            if session:
                s3_client = session.client('s3')
                bucket_name = f"myapp-data-{region}"
                
                # Deploy to region-specific bucket
                s3_client.put_object(
                    Bucket=bucket_name,
                    Key='data.json',
                    Body=json.dumps(data)
                )
                logging.info(f"Deployed to {region}")

Credential Rotation
-------------------

.. code-block:: python

    import time
    from datetime import datetime, timedelta
    from dtPyAppFramework.cloud import CloudSessionManager

    class CredentialRotationManager:
        def __init__(self):
            self.cloud_manager = CloudSessionManager()
            self.rotation_schedule = {}
        
        def schedule_rotation(self, session_name, rotation_hours=24):
            """Schedule credential rotation for a session."""
            next_rotation = datetime.now() + timedelta(hours=rotation_hours)
            self.rotation_schedule[session_name] = next_rotation
        
        def check_and_rotate_credentials(self):
            """Check if any credentials need rotation."""
            current_time = datetime.now()
            
            for session_name, rotation_time in self.rotation_schedule.items():
                if current_time >= rotation_time:
                    self.rotate_session_credentials(session_name)
        
        def rotate_session_credentials(self, session_name):
            """Rotate credentials for a specific session."""
            try:
                # Implementation depends on cloud provider
                # This would typically involve:
                # 1. Creating new temporary credentials
                # 2. Updating the session
                # 3. Invalidating old credentials
                logging.info(f"Rotating credentials for session: {session_name}")
                
                # Reschedule next rotation
                self.schedule_rotation(session_name)
                
            except Exception as ex:
                logging.error(f"Failed to rotate credentials for {session_name}: {ex}")

Error Handling and Monitoring
=============================

Session Health Monitoring
--------------------------

.. code-block:: python

    from dtPyAppFramework.cloud import CloudSessionManager
    import logging

    def monitor_cloud_session_health():
        """Monitor health of all configured cloud sessions."""
        cloud_manager = CloudSessionManager()
        health_report = {}
        
        for session in cloud_manager.sessions:
            session_name = session.name
            
            try:
                if session.session_type == "aws":
                    # Test AWS session
                    aws_session = cloud_manager.get_session(session_name)
                    sts_client = aws_session.client('sts')
                    identity = sts_client.get_caller_identity()
                    
                    health_report[session_name] = {
                        'status': 'healthy',
                        'identity': identity.get('Arn'),
                        'account': identity.get('Account')
                    }
                    
                elif session.session_type == "azure":
                    # Test Azure session
                    azure_session = cloud_manager.get_session(session_name)
                    # Perform Azure health check (implementation specific)
                    
                    health_report[session_name] = {
                        'status': 'healthy',
                        'subscription': session.subscription_id
                    }
                    
            except Exception as ex:
                health_report[session_name] = {
                    'status': 'unhealthy',
                    'error': str(ex)
                }
                logging.error(f"Session {session_name} health check failed: {ex}")
        
        return health_report

Retry and Circuit Breaker Patterns
----------------------------------

.. code-block:: python

    import time
    import random
    from functools import wraps

    def cloud_service_retry(max_retries=3, backoff_factor=2):
        """Decorator for retrying cloud service calls with exponential backoff."""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                last_exception = None
                
                for attempt in range(max_retries):
                    try:
                        return func(*args, **kwargs)
                    except Exception as ex:
                        last_exception = ex
                        
                        if attempt < max_retries - 1:
                            # Exponential backoff with jitter
                            delay = backoff_factor ** attempt + random.uniform(0, 1)
                            logging.warning(f"Attempt {attempt + 1} failed, retrying in {delay:.2f}s: {ex}")
                            time.sleep(delay)
                        else:
                            logging.error(f"All {max_retries} attempts failed")
                            raise last_exception
                
                return None
            return wrapper
        return decorator

    @cloud_service_retry(max_retries=3)
    def robust_s3_upload(file_path, bucket, key):
        """S3 upload with automatic retry logic."""
        from dtPyAppFramework.cloud import CloudSessionManager
        
        cloud_manager = CloudSessionManager()
        aws_session = cloud_manager.get_session("aws_primary")
        
        s3_client = aws_session.client('s3')
        s3_client.upload_file(file_path, bucket, key)

Best Practices
==============

1. **Environment-Specific Sessions**: Use different sessions for dev/staging/production
2. **Principle of Least Privilege**: Grant only necessary permissions to cloud sessions
3. **Credential Rotation**: Implement regular credential rotation for security
4. **Error Handling**: Implement proper retry logic and error handling
5. **Monitoring**: Monitor session health and authentication failures
6. **Configuration Security**: Store sensitive configuration in secrets, not config files
7. **Multi-Region Support**: Design for multi-region deployments when needed
8. **Session Lifecycle**: Properly manage session creation, usage, and cleanup

Security Considerations
=======================

Credential Management
---------------------

.. code-block:: yaml

    # Good - credentials from environment/secrets
    cloud_sessions:
      - name: "azure_production"
        session_type: "azure"
        subscription_id: "ENV/AZURE_SUBSCRIPTION_ID"  # Environment variable
        client_secret: "SEC/azure_client_secret"       # From secrets manager
        
    # Bad - credentials in configuration file
    cloud_sessions:
      - name: "azure_production"
        session_type: "azure"
        subscription_id: "12345678-1234-1234-1234-123456789012"
        client_secret: "super_secret_password"  # Never do this!

Access Control
--------------

Implement proper access control for cloud sessions:

.. code-block:: python

    from dtPyAppFramework.cloud import CloudSessionManager
    from dtPyAppFramework.settings import Settings

    def get_authorized_cloud_session(session_name, required_permissions=None):
        """Get cloud session with permission validation."""
        settings = Settings()
        user_role = settings.get('user.role')
        
        # Check if user has permission to use this session
        allowed_sessions = settings.get(f'roles.{user_role}.allowed_sessions', [])
        
        if session_name not in allowed_sessions:
            raise PermissionError(f"User role '{user_role}' not authorized for session '{session_name}'")
        
        cloud_manager = CloudSessionManager()
        return cloud_manager.get_session(session_name)

The cloud integration system provides a robust, secure foundation for multi-cloud application development while maintaining the framework's principles of configuration-driven setup and centralized management.
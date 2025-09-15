======================
Multiprocessing System
======================

The Multiprocessing System provides advanced process spawning, coordination, and monitoring capabilities with full framework integration, cross-process communication, and comprehensive process lifecycle management.

Overview
========

dtPyAppFramework's multiprocessing system is designed for applications that need to scale across multiple CPU cores while maintaining framework benefits like configuration access, secrets management, and coordinated logging across all processes.

Key Features:

* **Framework-Integrated Processes**: Spawned processes inherit full framework capabilities
* **Cross-Process Configuration**: Shared settings and secrets across all processes
* **Coordinated Logging**: Each process gets its own log context while maintaining coordination
* **Process Lifecycle Management**: Automatic process monitoring, cleanup, and error handling
* **Inter-Process Communication**: Pipes and shared state management
* **Job Management**: Organized job-based process grouping with unique identifiers

Core Components
===============

MultiProcessingManager
----------------------

The ``MultiProcessingManager`` class is the main interface for creating and managing multiprocessing jobs.

.. autoclass:: dtPyAppFramework.process.multiprocessing.MultiProcessingManager
   :members:
   :inherited-members:

Key Features:

**Singleton Pattern**
  Only one manager instance exists per application, ensuring centralized process coordination.

**Job Management**
  Creates and tracks multiprocessing jobs with unique identifiers and organized process groups.

**Log Path Integration**
  Automatically integrates with the logging system to provide process-specific log directories.

MultiProcessingJob
------------------

The ``MultiProcessingJob`` class represents a group of related worker processes.

.. autoclass:: dtPyAppFramework.process.multiprocessing.MultiProcessingJob
   :members:

Key Features:

**Unique Job Identification**
  Each job gets a unique UUID for tracking and log organization.

**Worker Process Management**
  Manages multiple worker processes as a coordinated unit.

**Framework Integration**
  Each worker process is automatically initialized with full framework capabilities.

Process Detection
=================

Spawned Process Detection
-------------------------

.. py:function:: dtPyAppFramework.process.is_multiprocess_spawned_instance()

   Detect whether the current process is a spawned instance in a multiprocessing environment.

   :return: True if the process is a spawned instance, False if main process
   :rtype: bool

**Detection Logic:**
- Checks if process name is not "MainProcess"
- Looks for ``--multiprocessing-fork`` command line argument
- Used throughout framework for process-specific initialization

.. code-block:: python

    from dtPyAppFramework.process import is_multiprocess_spawned_instance
    import logging

    if is_multiprocess_spawned_instance():
        logging.info("Running in spawned process context")
    else:
        logging.info("Running in main process context")

UUID Management
---------------

.. py:function:: dtPyAppFramework.process.multiprocessing.get_new_uuid()

   Generate a new UUID ensuring uniqueness across the application.

   :return: A new UUID string
   :rtype: str

**Features:**
- Maintains list of issued UUIDs to prevent duplicates
- Thread-safe UUID generation
- Used for job identification and process tracking

Basic Usage
===========

Creating Multiprocessing Jobs
-----------------------------

.. code-block:: python

    from dtPyAppFramework.application import AbstractApp
    from dtPyAppFramework.process import MultiProcessingManager
    import logging

    class MyApplication(AbstractApp):
        def main(self, args):
            # Get the multiprocessing manager
            manager = MultiProcessingManager()
            
            # Create a multiprocessing job
            job = manager.new_multiprocessing_job(
                job_name="data_processing",
                worker_count=4,
                target=self.process_data_batch,
                args=(data_to_process,),
                kwargs={'batch_size': 100}
            )
            
            # Start the job
            job.start()
            
            # Wait for completion
            job.join()
            
            logging.info("All workers completed")

        def process_data_batch(self, data, batch_size=50):
            """Function executed by each worker process."""
            import logging
            
            # This runs in a spawned process with full framework access
            logger = logging.getLogger(__name__)
            logger.info(f"Worker started processing {len(data)} items")
            
            # Access configuration and secrets in spawned process
            from dtPyAppFramework.settings import Settings
            settings = Settings()
            
            api_key = settings.get('SEC/api_key')  # Secrets available
            timeout = settings.get('processing.timeout', 30)  # Config available
            
            # Process data in batches
            for i in range(0, len(data), batch_size):
                batch = data[i:i+batch_size]
                self.process_batch(batch, api_key, timeout)
                logger.info(f"Processed batch {i//batch_size + 1}")

Worker Process Lifecycle
========================

Framework Initialization in Workers
------------------------------------

Each spawned worker process goes through automatic framework initialization:

1. **Process Detection**: Framework detects spawned process context
2. **Path Initialization**: Worker-specific paths and directories created
3. **Settings Initialization**: Configuration loaded with cross-process sharing
4. **Logging Setup**: Process-specific logging context established
5. **Secrets Loading**: Secrets manager initialized with shared state
6. **Target Function Execution**: User's worker function called

**Automatic Framework Setup:**

.. code-block:: python

    def worker_function(data):
        """User-defined worker function."""
        # Framework is already initialized when this function starts
        
        import logging
        from dtPyAppFramework.settings import Settings
        from dtPyAppFramework.paths import ApplicationPaths
        
        # All framework components are available
        logger = logging.getLogger(__name__)
        settings = Settings()
        paths = ApplicationPaths()
        
        # Worker-specific log directory
        logger.info(f"Worker logging to: {paths.logging_root_path}")
        
        # Process data with full framework support
        api_endpoint = settings.get('api.endpoint')
        database_url = settings.get('SEC/database_url')
        
        # Worker processing logic here
        process_data(data, api_endpoint, database_url)

Cross-Process Communication
===========================

Shared Configuration
--------------------

Configuration and secrets are automatically shared across processes through inter-process communication:

.. code-block:: python

    class MyApplication(AbstractApp):
        def main(self, args):
            from dtPyAppFramework.settings import Settings
            
            # Main process configuration
            settings = Settings()
            
            # Add runtime configuration that will be shared
            settings.set('runtime.job_id', 'job_12345')
            settings.secret_manager.set_secret('runtime_token', 'temp_token_value')
            
            # Spawn workers - they automatically get shared config
            manager = MultiProcessingManager()
            job = manager.new_multiprocessing_job(
                job_name="shared_config_job",
                worker_count=2,
                target=worker_with_shared_config
            )
            job.start()

    def worker_with_shared_config():
        """Worker function with access to shared configuration."""
        from dtPyAppFramework.settings import Settings
        
        settings = Settings()
        
        # Access configuration set by main process
        job_id = settings.get('runtime.job_id')  # 'job_12345'
        token = settings.secret_manager.get_secret('runtime_token')  # 'temp_token_value'
        
        print(f"Worker processing job: {job_id} with token: {token}")

Process Coordination
--------------------

Coordinate process execution with shared state:

.. code-block:: python

    from multiprocessing import Manager, Event
    import time

    def coordinated_worker_example():
        """Example of coordinated multiprocessing."""
        from dtPyAppFramework.process import MultiProcessingManager
        
        # Create shared objects for coordination
        mp_manager = Manager()
        shared_counter = mp_manager.Value('i', 0)
        coordination_event = mp_manager.Event()
        
        # Create processing job
        job_manager = MultiProcessingManager()
        job = job_manager.new_multiprocessing_job(
            job_name="coordinated_processing",
            worker_count=3,
            target=coordinated_worker,
            args=(shared_counter, coordination_event)
        )
        
        # Start workers
        job.start()
        
        # Coordinate from main process
        time.sleep(2)  # Let workers initialize
        coordination_event.set()  # Signal workers to start processing
        
        # Wait for completion
        job.join()

    def coordinated_worker(shared_counter, coordination_event):
        """Worker that coordinates with other processes."""
        import logging
        
        logger = logging.getLogger(__name__)
        logger.info("Worker initialized, waiting for coordination signal")
        
        # Wait for coordination signal
        coordination_event.wait()
        
        # Perform coordinated work
        with shared_counter.get_lock():
            current_value = shared_counter.value
            shared_counter.value = current_value + 1
            logger.info(f"Worker incremented counter to {shared_counter.value}")

Advanced Usage Patterns
========================

Job Queuing and Management
---------------------------

Implement job queuing for complex workflows:

.. code-block:: python

    from queue import Queue
    from threading import Thread
    import time

    class JobQueueManager:
        def __init__(self):
            self.job_queue = Queue()
            self.active_jobs = {}
            self.mp_manager = MultiProcessingManager()
            
        def submit_job(self, job_name, worker_count, target_function, *args, **kwargs):
            """Submit a job to the queue."""
            job_spec = {
                'job_name': job_name,
                'worker_count': worker_count,
                'target': target_function,
                'args': args,
                'kwargs': kwargs
            }
            self.job_queue.put(job_spec)
            
        def process_job_queue(self, max_concurrent_jobs=2):
            """Process jobs from queue with concurrency limit."""
            while not self.job_queue.empty() or self.active_jobs:
                # Start new jobs if under limit
                while (len(self.active_jobs) < max_concurrent_jobs and 
                       not self.job_queue.empty()):
                    job_spec = self.job_queue.get()
                    
                    job = self.mp_manager.new_multiprocessing_job(**job_spec)
                    job.start()
                    
                    self.active_jobs[job.job_id] = job
                    logging.info(f"Started job: {job_spec['job_name']}")
                
                # Check for completed jobs
                completed_jobs = []
                for job_id, job in self.active_jobs.items():
                    if not job.is_alive():
                        completed_jobs.append(job_id)
                
                # Remove completed jobs
                for job_id in completed_jobs:
                    job = self.active_jobs.pop(job_id)
                    logging.info(f"Job {job.job_name} completed")
                
                time.sleep(0.5)  # Brief pause between checks

Error Handling and Recovery
---------------------------

Implement robust error handling for multiprocessing scenarios:

.. code-block:: python

    import logging
    from multiprocessing import Process
    import traceback

    def resilient_worker(data, max_retries=3):
        """Worker function with error handling and retries."""
        logger = logging.getLogger(__name__)
        
        for attempt in range(max_retries):
            try:
                # Worker processing logic
                result = process_data_with_retries(data)
                logger.info(f"Worker completed successfully on attempt {attempt + 1}")
                return result
                
            except Exception as ex:
                logger.error(f"Worker attempt {attempt + 1} failed: {ex}")
                logger.error(traceback.format_exc())
                
                if attempt < max_retries - 1:
                    logger.info(f"Retrying in {2 ** attempt} seconds...")
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    logger.error("Max retries exceeded, worker failed")
                    raise

    def monitor_job_health(job, timeout_seconds=300):
        """Monitor job health and handle failures."""
        import time
        
        start_time = time.time()
        
        while job.is_alive():
            # Check for timeout
            if time.time() - start_time > timeout_seconds:
                logging.error(f"Job {job.job_name} timed out, terminating")
                job.terminate()
                job.join(timeout=10)  # Give it time to clean up
                break
                
            # Check worker health
            dead_workers = [w for w in job.workers if not w.is_alive()]
            if dead_workers:
                logging.warning(f"Job {job.job_name} has {len(dead_workers)} dead workers")
            
            time.sleep(5)  # Check every 5 seconds

Performance Optimization
========================

Process Pool Management
-----------------------

Optimize process creation and reuse:

.. code-block:: python

    from multiprocessing import Pool
    from functools import partial

    class OptimizedProcessManager:
        def __init__(self, process_count=None):
            if process_count is None:
                from dtPyAppFramework.settings import Settings
                settings = Settings()
                process_count = settings.get('multiprocessing.max_workers', 4)
                
            self.process_count = process_count
            self.pool = None
            
        def __enter__(self):
            self.pool = Pool(processes=self.process_count)
            return self
            
        def __exit__(self, exc_type, exc_val, exc_tb):
            if self.pool:
                self.pool.close()
                self.pool.join()
                
        def map_job(self, function, iterable, chunk_size=None):
            """Map function over iterable using process pool."""
            if chunk_size is None:
                chunk_size = max(1, len(iterable) // (self.process_count * 4))
                
            return self.pool.map(function, iterable, chunksize=chunk_size)

    # Usage
    def batch_processor(items):
        """Process items in batches using optimized process pool."""
        with OptimizedProcessManager() as manager:
            # Process items in parallel
            results = manager.map_job(process_single_item, items)
            return results

Memory Management
-----------------

Handle memory-intensive multiprocessing workloads:

.. code-block:: python

    import psutil
    import gc
    import logging

    def memory_aware_worker(data_chunk, memory_limit_mb=512):
        """Worker that monitors and manages memory usage."""
        logger = logging.getLogger(__name__)
        process = psutil.Process()
        
        for item in data_chunk:
            # Check memory usage before processing
            memory_mb = process.memory_info().rss / (1024 * 1024)
            
            if memory_mb > memory_limit_mb:
                logger.warning(f"Memory usage ({memory_mb:.1f}MB) exceeds limit, forcing GC")
                gc.collect()
                memory_mb = process.memory_info().rss / (1024 * 1024)
                
                if memory_mb > memory_limit_mb:
                    logger.error(f"Memory usage still high ({memory_mb:.1f}MB), may need tuning")
            
            # Process the item
            result = process_item(item)
            
            # Periodic cleanup
            if hasattr(item, '__del__'):
                del item

Windows Service Integration
===========================

The multiprocessing system integrates with Windows service support:

.. code-block:: python

    class ServiceApp(AbstractApp):
        def main(self, args):
            """Main application that can run as service or console."""
            import logging
            
            logger = logging.getLogger(__name__)
            
            if self.console_app:
                logger.info("Running in console mode")
            else:
                logger.info("Running as Windows service")
            
            # Create multiprocessing job
            manager = MultiProcessingManager()
            job = manager.new_multiprocessing_job(
                job_name="service_workers",
                worker_count=2,
                target=self.service_worker
            )
            
            # Start background processing
            job.start()
            
            # Keep service running
            while self.running.is_set():
                time.sleep(1)
                
            # Cleanup on service stop
            job.terminate()
            job.join()

Best Practices
==============

1. **Process Count**: Use CPU count as default, allow configuration override
2. **Error Handling**: Implement retry logic and graceful failure handling
3. **Resource Management**: Monitor memory usage and clean up resources
4. **Logging**: Use process-specific loggers for debugging
5. **Configuration**: Share configuration through framework, not global variables
6. **Coordination**: Use proper synchronization primitives for shared state
7. **Testing**: Test multiprocessing code with different worker counts
8. **Monitoring**: Implement health checks for long-running processes

Common Patterns
===============

Map-Reduce Pattern
------------------

.. code-block:: python

    def map_reduce_example(data, map_function, reduce_function):
        """Implement map-reduce pattern with multiprocessing."""
        from dtPyAppFramework.process import MultiProcessingManager
        import multiprocessing
        
        # Split data into chunks
        chunk_size = len(data) // multiprocessing.cpu_count()
        chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]
        
        # Map phase - process chunks in parallel
        manager = MultiProcessingManager()
        
        # Use multiprocessing.Manager for result collection
        mp_manager = multiprocessing.Manager()
        results_dict = mp_manager.dict()
        
        def map_worker(chunk_data, chunk_id):
            result = [map_function(item) for item in chunk_data]
            results_dict[chunk_id] = result
        
        # Create and start map jobs
        map_jobs = []
        for i, chunk in enumerate(chunks):
            job = manager.new_multiprocessing_job(
                job_name=f"map_job_{i}",
                worker_count=1,
                target=map_worker,
                args=(chunk, i)
            )
            job.start()
            map_jobs.append(job)
        
        # Wait for map phase completion
        for job in map_jobs:
            job.join()
        
        # Reduce phase - combine results
        all_results = []
        for chunk_id in sorted(results_dict.keys()):
            all_results.extend(results_dict[chunk_id])
        
        return reduce_function(all_results)

The multiprocessing system provides a powerful foundation for scaling Python applications across multiple CPU cores while maintaining the benefits of the dtPyAppFramework's integrated configuration, logging, and secrets management capabilities.
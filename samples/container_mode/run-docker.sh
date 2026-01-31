#!/bin/bash
# Convenience script for running the container mode sample with Docker

set -e

# Colour codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Colour

# Configuration
IMAGE_NAME="dtpyapp-container-sample"
CONTAINER_NAME="dtpyapp-sample"
DOCKERFILE_PATH="."

# Function to print coloured output
print_status() {
    local message="$1"
    echo -e "${BLUE}[INFO]${NC} $message"
    return 0
}

print_success() {
    local message="$1"
    echo -e "${GREEN}[SUCCESS]${NC} $message"
    return 0
}

print_warning() {
    local message="$1"
    echo -e "${YELLOW}[WARNING]${NC} $message"
    return 0
}

print_error() {
    local message="$1"
    echo -e "${RED}[ERROR]${NC} $message" >&2
    return 0
}

# Function to check if Docker is running
check_docker() {
    if ! docker info >/dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
    print_success "Docker is running"
    return 0
}

# Function to build the Docker image
build_image() {
    local image_name="$IMAGE_NAME"
    local dockerfile_path="$DOCKERFILE_PATH"
    print_status "Building Docker image: $image_name"
    print_status "Using main project requirements.txt for dependencies"

    # Build from the project root to include the framework source and requirements.txt
    docker build -t "$image_name" -f "$dockerfile_path/Dockerfile" ../..

    if [[ $? -eq 0 ]]; then
        print_success "Docker image built successfully"
        print_success "All dependencies from ../../requirements.txt installed"
    else
        print_error "Failed to build Docker image"
        exit 1
    fi
    return 0
}

# Function to run the container
run_container() {
    local mode=${1:-"demo"}

    print_status "Running container in $mode mode"

    # Remove existing container if it exists
    docker rm -f "$CONTAINER_NAME" 2>/dev/null || true

    # Set command based on mode
    local cmd=""
    case $mode in
        "demo")
            cmd="python sample/container_app.py --container --demo-mode"
            ;;
        "config")
            cmd="python sample/container_app.py --container --task config"
            ;;
        "secrets")
            cmd="python sample/container_app.py --container --task secrets"
            ;;
        "resources")
            cmd="python sample/container_app.py --container --task resources"
            ;;
        "interactive")
            # Run interactive shell
            docker run -it --rm \
                --name "$CONTAINER_NAME" \
                -v "$(pwd)/data:/app/data" \
                -v "$(pwd)/logs:/app/logs" \
                -e CONTAINER_MODE=true \
                "$IMAGE_NAME" \
                /bin/bash
            return 0
            ;;
        *)
            print_error "Unknown mode: $mode"
            echo "Available modes: demo, config, secrets, resources, interactive" >&2
            exit 1
            ;;
    esac

    # Run the container
    docker run --rm \
        --name "$CONTAINER_NAME" \
        -v "$(pwd)/data:/app/data" \
        -v "$(pwd)/logs:/app/logs" \
        -e CONTAINER_MODE=true \
        -e DB_HOST=localhost \
        -e API_KEY=demo-key-123 \
        "$IMAGE_NAME" \
        $cmd
    return 0
}

# Function to run with Docker Compose
run_compose() {
    print_status "Running with Docker Compose (full stack)"

    if [[ ! -f "docker-compose.yml" ]]; then
        print_error "docker-compose.yml not found"
        exit 1
    fi

    # Build and start all services
    docker-compose up --build
    return 0
}

# Function to clean up Docker resources
cleanup() {
    local remove_flag="$1"
    print_status "Cleaning up Docker resources"

    # Stop and remove containers
    docker rm -f "$CONTAINER_NAME" 2>/dev/null || true
    docker-compose down 2>/dev/null || true

    # Remove image if requested
    if [[ "$remove_flag" == "--remove-image" ]]; then
        docker rmi "$IMAGE_NAME" 2>/dev/null || true
        print_success "Removed Docker image"
    fi

    print_success "Cleanup completed"
    return 0
}

# Function to show container logs
show_logs() {
    print_status "Showing logs for container: $CONTAINER_NAME"
    docker logs -f "$CONTAINER_NAME"
    return 0
}

# Function to show usage
usage() {
    cat << EOF
Usage: $0 [COMMAND] [OPTIONS]

Commands:
    build                 Build the Docker image
    run [MODE]           Run the container (modes: demo, config, secrets, resources, interactive)
    compose              Run with Docker Compose (full stack)
    logs                 Show container logs
    cleanup              Clean up containers and networks
    cleanup --remove-image  Also remove the built image
    help                 Show this help message

Examples:
    $0 build                    # Build the image
    $0 run                      # Run in demo mode
    $0 run config               # Run config demonstration
    $0 run interactive          # Run interactive shell
    $0 compose                  # Run full stack with Docker Compose
    $0 cleanup                  # Clean up resources

EOF
    return 0
}

# Main script logic
case "${1:-help}" in
    "build")
        check_docker
        build_image
        ;;
    "run")
        check_docker
        run_container "${2:-demo}"
        ;;
    "compose")
        check_docker
        run_compose
        ;;
    "logs")
        check_docker
        show_logs
        ;;
    "cleanup")
        check_docker
        cleanup "$2"
        ;;
    "help"|"--help"|"-h")
        usage
        ;;
    *)
        print_error "Unknown command: $1"
        usage
        exit 1
        ;;
esac

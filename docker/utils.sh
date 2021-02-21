#!/bin/bash

check_dependencies ()
{
    set -e
    [[ -x "$(which docker)" ]] || (echo -e "\e[33mDocker isn't installed\e[0m" && exit 1)
    set +e
}


create_docker_network ()
{
    if [[ ! "$(docker network ls -q -f name=opac-net)" ]]; then
        if docker network create --driver bridge opac-net 2>/dev/null; then
            echo -e "\e[32mDocker 'opac-net' network created\e[0m"
        fi
    fi
}


build_docker_image ()
{
    echo -e "\e[36mBuilding docker image\e[0m"

    local self_path=$(dirname "$0")
    local dockerfile_path=$(realpath "$self_path/Dockerfile")
    set -e
    [[ -f "$dockerfile_path" ]] || (echo -e "\e[33mDockerfile doesn't exist\e[0m" && exit 1)
    set +e

    docker build --quiet --tag $1 --file $dockerfile_path . 1>/dev/null
    docker image prune -f 1>/dev/null
}


check_running_container ()
{
    sleep 2

    if [[ "$(docker ps -q -f name=$1)" ]];
    then
        echo -e "\e[32mContainer '$1' started\e[0m"
    else
        local code=$?
        echo -e "\e[31mContainer '$1' not started\e[0m"
        docker logs "$1"
        exit $code
    fi
}


stop_container ()
{
    if [[ "$(docker ps -q -f name=$1)" ]]; then
        docker stop -t 0 $1
    fi
    docker container prune -f 1>/dev/null
}

create_config_file ()
{
    local config_path=$(realpath "$1/config.ini")
    local config_example_path=$(realpath "$1/config.ini.example")
    if [[ ! -f "$config_path" && -f "$config_example_path" ]]; then
        echo -e "\e[36mCreating config file\e[0m"
        cp $config_example_path $config_path;
    fi
}

run_tests ()
{
    echo -e "\e[36mStarting $1 tests\e[0m"

    docker run \
        --rm \
        --name "$1-tests" \
        "$1:latest" \
        python setup.py pytest
}

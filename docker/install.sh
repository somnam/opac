#!/bin/bash

source ./docker/utils.sh


main ()
{
    check_docker

    [[ $(docker_compose_installed) = true ]] || install_docker_compose

    [[ $? -eq 0 ]] || (echo -e "\e[33mDocker compose not installed\e[0m" && exit 1)

    echo -e "\e[36mDocker compose installed\e[0m"

    [[ $(docker_compose_works) = true ]] || (echo -e "\e[33mDocker compose not working\e[0m" && exit 1)

    echo -e "\e[36mDocker compose works\e[0m"
}


main
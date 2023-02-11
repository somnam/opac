#!/bin/bash

check_docker ()
{
    set -e

    [[ -x "$(which docker)" ]] || (echo -e "\e[33mDocker not installed\e[0m" && exit 1)

    set +e
}


docker_compose_path ()
{
    echo "$HOME/.docker/cli-plugins"
}


docker_compose_file_path ()
{
    echo "$(docker_compose_path)/docker-compose"
}


docker_compose_installed ()
{
    set -e

    local compose_installed=false

    [[ -f "$(docker_compose_file_path)" ]] && compose_installed=true

    echo "$compose_installed"

    set +e
}


docker_compose_works ()
{
    local compose_works=false
    local docker=$(which docker)

    $docker compose &>/dev/null

    [[ $? -eq 0 ]] && compose_works=true

    echo "$compose_works"
}


install_docker_compose ()
{
    set -e

    local wget=$(which wget)
    local grep=$(which grep)
    local cut=$(which cut)

    local release_url="https://api.github.com/repos/docker/compose/releases/latest"

    local download_url=$(
        $wget -q -O- $release_url \
            | $grep "browser_download_url.*docker-compose-linux-x86_64[^\.]" \
            | $cut -d \" -f 4
    )

    [[ -n $download_url ]] || (echo -e "\e[33mDocker compose download url not found\e[0m" && exit 1)

    local mkdir=$(which mkdir)
    local chmod=$(which chmod)

    echo -e "\e[36mDownloading docker compose\e[0m"

    $mkdir -p $(docker_compose_path) && \
        $wget -q $download_url -O $(docker_compose_file_path) && \
        $chmod u+x $(docker_compose_file_path)

    set +e
}


check_docker_compose ()
{
    set -e

    [[ $(docker_compose_installed) = true ]] || (echo -e "\e[33mDocker compose not installed\e[0m" && exit 1)

    [[ $(docker_compose_works) = true ]] || (echo -e "\e[33mDocker compose not working\e[0m" && exit 1)

    set +e
}


create_config_file ()
{
    set -e

    local cp=$(which cp)
    local config_path=$(realpath "$1/config.ini")
    local config_example_path=$(realpath "$1/config.ini.example")

    if [[ ! -f "$config_path" && -f "$config_example_path" ]]; then
        echo -e "\e[36mCreating config file\e[0m"
        $cp $config_example_path $config_path;
    fi

    set +e
}

#!/bin/bash

source ./docker/utils.sh


main ()
{
    check_docker_compose

    local docker=$(which docker)

    $docker compose build server && \
        $docker compose run --rm server bash -c "python -mpip install --user tox && tox"
}


main
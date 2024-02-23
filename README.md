# alephium-stats-backend

## Overview

This backend service is designed to support the Alephium blockchain network by performing two primary tasks: delivering data for a statistics frontend and providing real-time updates on new blocks through a WebSocket for the visualizer. This service leverages the power of Python, Celery, Redis and WebSocket technologies to offer a seamless and efficient data flow for Alephium network visualizations and analytics. Furthermore, within the extensive repository, detailed notes are available to facilitate the effortless integration of the database into our system architecture. Our upcoming development roadmap includes the implementation of a robust database system designed to securely store aggregated statistical data. The infrastructure is already poised to seamlessly support this feature upon deployment.

## Development

### Install

    #REDIS
    sudo apt install redis
    sudo systemctl enable redis
    sudo systemctl start redis

    # install lets-cli https://github.com/lets-cli/lets/releases

    # install sql-packages
    sqlite
    haskell-persistent-sqlite

    # folder structure
    add in root directory folder ```data``` for openapi and sql stuff


    # install poetry 2 Options
    sudo apt install python311
    pip3 install --user poetry

    # cd repo dir
    poetry install
    git submodule update --init --recursive
    cd contracts
    npm i
    cd ..

    # add further packages
    poetry add {package_name}

### Run

    # start everthing in separate terminal
    # before each cmd run:
    lets env # enables virtual env

    # the backend runs on localhost:8000, exposed to the user
    lets run backend

     # performs async heavy lifting
    lets run worker

    # pushes periodic cmds to the worker
    lets run beat

    # check docs of the backend
    localhost:8000/docs

### DB Upgrade

    # NOTE:actual no db necessary

    # start / stop the db
    lets db <start/stop>

    # apply all previous upgrades
    lets db upgrade

    # apply all previous downgrades
    lets db downgrade

    # create a revision
    msg="<some msg and WHAT THE FUCK YOU EVENT DID HERE> lets db revision

    # some files were added to the alembic folder
    git commit -m "chore(alembic): blabla what you did

    # procedure
    lets db start
    lets db upgrade
    lets db revision
    lets db upgrade (maybe you have to add the import sqlmodel)
    commit everything

### OPENAPI

    # install openapi-generator in project root directory
    npm install @openapitools/openapi-generator-cli

    # generate openapi clients
    client directory: npm install
    backend directory: lets client

### TEST

    # run the tests
    lets test

    # run coverage
    lets cov

## VERSIONING

This repository strictly uses [conventional
commits](https://bitbucket.org/blog/pipelines-manual-steps-confidence-deployment-pipeline).
As such, a pre-commit hook checks your commit message.

## Pre-commit hooks

We highly encourage you to install pre-commit hooks and **also** enable access
to commit messages via:

    pre-commit install
    pre-commit install --hook-type commit-msg

Optionally, you may want to use
[commitizen](https://github.com/commitizen-tools/commitizen) and `cz c` to
construct your commit messages.

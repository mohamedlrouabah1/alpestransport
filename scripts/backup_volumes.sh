#!/bin/bash

# Use loomchild/volume-backup to backup every Wikibase volumes (mediawiki-images, mediawiki-mysql, query-service, quickstatements)

DOCKER_COMPOSE_NAME="eurhisfirm-wikibase-docker"

if [ "$1" == "" ]; then
    echo "usage: $0 {target_dir}"
    exit 1
fi
TARGET_DIR=$1

if [ ! -e $TARGET_DIR ]; then
    echo "Target dir [$TARGET_DIR] not found"
    exit 1
fi

backup_volume() {
    local volume_name="$1"
    echo "Dumping ${volume_name}..."
    docker run -v ${DOCKER_COMPOSE_NAME}_${volume_name}:/volume -v ${TARGET_DIR}:/backup --rm loomchild/volume-backup backup ${volume_name}
    echo "Done."
}

backup_volume mediawiki-images-data
backup_volume mediawiki-mysql-data
backup_volume query-service-data
backup_volume quickstatements-data

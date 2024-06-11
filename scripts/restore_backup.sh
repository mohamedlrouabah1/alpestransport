#!/bin/bash

# Use loomchild/volume-restore to restore backups of every Wikibase volumes (mediawiki-images, mediawiki-mysql, query-service, quickstatements)

if [ "$1" == "" ]; then
	echo "usage: $0 {backup_dir}"
	exit 1
fi

BACKUP_DIR=$1

if [ ! -e "$BACKUP_DIR" ]; then
	echo "Backup dir [$BACKUP_DIR] not found."
	exit 1
fi

function restore_volume() {
	local volume_name="$1"
	echo "Restoring ${volume_name}..."
	docker run -v eurhisfirm-wikibase-docker_${volume_name}:/volume -v $BACKUP_DIR:/backup --rm loomchild/volume-backup restore ${volume_name}
	echo "done."
}

restore_volume mediawiki-images-data
restore_volume mediawiki-mysql-data
restore_volume query-service-data
restore_volume quickstatements-data

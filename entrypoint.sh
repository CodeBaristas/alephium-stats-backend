#!/usr/bin/env sh

main() {
	# NOTE:actual no db necessary
	# alembic upgrade head

	case "$APP_PART" in
	backend)
		unbuffer python3 -m $PACKAGE.run_$APP_PART
		;;
	worker)
		unbuffer celery --app=alephium_stats.run_worker.celery worker -l error -c 4
		;;
	beat)
		unbuffer celery --app=alephium_stats.run_worker.celery beat -l error
		;;
	*)
		echo "usage: <backend/worker/beat>"
		;;
	esac
}
main $@

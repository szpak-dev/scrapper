until make download t=marttiini; do
    echo "Program 'download' crashed with exit code $?.  Respawning.." >&2
    sleep 1
done
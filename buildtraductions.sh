echo "[i] Initialized\n"
echo "[i] Building spanish traductions..."
cd locales/es/LC_MESSAGES/
msgfmt -o base.mo base
echo "[i] Building english traduction..."
cd ../../eng/LC_MESSAGES/
msgfmt -o base.mo base
echo "[i] Going back to root dir..."
cd ../../..
echo "[i] Finished building traductions. Have a good day"


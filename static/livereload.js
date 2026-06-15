// Dev-only live reload: poll the server's id and, when it changes (the dev
// server restarted after a file edit), refresh THIS tab instead of letting a
// new one be opened. Included only when the server runs unfrozen.
(function () {
    let knownId = null;

    async function check() {
        try {
            const res = await fetch("/livereload", { cache: "no-store" });
            if (!res.ok) return;
            const { id } = await res.json();
            if (knownId === null) {
                knownId = id;            // first poll: remember the current server
            } else if (id !== knownId) {
                location.reload();       // server restarted -> refresh this tab
            }
        } catch (e) {
            // Server is mid-restart and briefly unreachable; ignore and retry.
        }
    }

    setInterval(check, 1000);
    check();
})();

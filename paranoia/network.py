"""
network.py
All UDP networking for Paranoia.

NetworkClient wraps the socket, handles the connect handshake,
polls the server until the game starts, and exchanges per-frame
state updates.
"""

from __future__ import annotations

import json
import socket
from time import time
from typing import TYPE_CHECKING

from paranoia.constants import (
    ENCODING, SERVER_PORT,
    CONNECT_MSG, CHECK_START_MSG, NOT_START_MSG,
    SEND_INTERVAL, RECV_BUFFER,
)

if TYPE_CHECKING:
    from paranoia.entities.player   import Player
    from paranoia.entities.opponent import Opponent
    from paranoia.entities.powerup  import Powerup


def get_lan_ip() -> str:
    """Return this machine's LAN IP address, falling back to loopback."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"
    finally:
        s.close()


class StartPayload:
    """Parsed data returned by the server when all players are ready."""

    def __init__(
        self,
        players: list[str],
        powerup_spawns: list[tuple[int, int]],
        player_start: list[int],
    ) -> None:
        self.players        = players
        self.powerup_spawns = powerup_spawns
        self.player_start   = player_start


class NetworkClient:
    """UDP client for one game session."""

    def __init__(self, server_ip: str) -> None:
        self.local_ip    = get_lan_ip()
        self.server_addr = (server_ip, SERVER_PORT)
        self._socket     = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._last_sent  = time()

    # ── Handshake ─────────────────────────────────────────────────────────

    def connect(self) -> None:
        """Send the connect message and print the server's acknowledgement."""
        self._socket.sendto(CONNECT_MSG.encode(ENCODING), self.server_addr)
        data, _ = self._socket.recvfrom(RECV_BUFFER)
        print(f"Server: {data.decode(ENCODING)}")

    def wait_for_start(self) -> StartPayload:
        """
        Poll the server with CHECK_START_MSG until it returns a start payload.
        Blocks until the server signals the game can begin.
        Returns a StartPayload with player IPs, powerup spawn positions,
        and this client's starting grid cell.
        """
        while True:
            if self._throttle():
                payload = self._poll_start()
                if payload is not None:
                    return payload

    def _poll_start(self) -> StartPayload | None:
        """Send one check-start message; return a StartPayload or None."""
        self._socket.sendto(CHECK_START_MSG.encode(ENCODING), self.server_addr)
        data, _ = self._socket.recvfrom(RECV_BUFFER)
        data     = data.decode(ENCODING)

        if data == NOT_START_MSG:
            return None

        parts              = data.split("-")
        players            = parts[0].split()
        powerup_spawns_raw = parts[1].split()
        player_start_raw   = parts[2]

        powerup_spawns = []
        for entry in powerup_spawns_raw:
            coords = entry.split(",")
            powerup_spawns.append((int(coords[0]), int(coords[1])))

        player_start = list(map(int, player_start_raw.split(",")))

        return StartPayload(players, powerup_spawns, player_start)

    # ── Per-frame update ──────────────────────────────────────────────────

    def send_recv_update(
        self,
        player: Player,
        opps: list[Opponent],
        powerups: list[Powerup],
    ) -> None:
        """
        Send the local player's state to the server and apply the
        returned opponent states to the opps list.
        """
        payload = {
            "x":             player.x,
            "y":             player.y,
            "powerups_name": player.powerups_name,
            "killed":        player.killed,
            "alive":         player.alive,
        }
        self._socket.sendto(json.dumps(payload).encode(ENCODING), self.server_addr)

        raw, _   = self._socket.recvfrom(RECV_BUFFER)
        updates  = json.loads(raw)

        for ip, info in updates.items():
            if ip == self.local_ip:
                continue
            for opp in opps:
                if opp.ip == ip:
                    opp.update(
                        info["x"],
                        info["y"],
                        info["powerups_name"],
                        info["killed"],
                        info["alive"],
                        powerups=powerups,
                        local_player=player,
                        all_opponents=opps,
                    )

    # ── Rate limiting ─────────────────────────────────────────────────────

    def _throttle(self) -> bool:
        """Return True and reset the timer if SEND_INTERVAL has elapsed."""
        now = time()
        if now >= self._last_sent + SEND_INTERVAL:
            self._last_sent = now
            return True
        return False

    def should_send(self) -> bool:
        """Public wrapper around _throttle for the game loop."""
        return self._throttle()


# ── Testing ───────────────────────────────────────────────────────────────

# Hardcoded spawn positions that mirror a normal server payload.
# Adjust player_start if you want to begin in a different part of the map.
_TEST_PAYLOAD = StartPayload(
    players        = [],                          # no opponents
    powerup_spawns = [                            # same positions the server assigns
        (30, 30), (70, 30), (30, 70),
        (70, 70), (50, 20), (20, 50),
    ],
    player_start   = [4, 4],                    # one of the predefined spawn cells
)


class DummyNetworkClient:
    """
    Drop-in replacement for NetworkClient used when TESTING = True.
    No socket is opened; all network methods are silent no-ops.
    """

    local_ip: str = get_lan_ip()

    def connect(self) -> None:
        print("[TESTING] Skipping server connection.")

    def wait_for_start(self) -> StartPayload:
        print("[TESTING] Starting solo — no server required.")
        return _TEST_PAYLOAD

    def send_recv_update(self, player, opps, powerups) -> None:  # type: ignore[override]
        pass  # nothing to send or receive in solo mode

    def should_send(self) -> bool:
        return False  # suppresses the update call in the game loop entirely

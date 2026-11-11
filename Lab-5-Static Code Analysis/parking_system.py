"""Campus Parking Permit Manager.

This module manages parking permits for vehicles in zones A, B and C.
It can register, revoke, check expiry and scan for unauthorized vehicles.
"""

import json
import random
from datetime import datetime, timedelta

# Global state
permits = {}
ZONES = ["A", "B", "C"]


def register_permit(vehicle_plate, zone_id, zone_records=None):
    """Register a new parking permit for a vehicle in the given zone.

    Args:
        vehicle_plate (str): Vehicle registration number.
        zone_id (str): Parking zone (A, B or C).
        zone_records (list, optional): List to record the registration.

    Returns:
        str or None: Permit number if successful, otherwise None.
    """
    if zone_records is None:
        zone_records = []

    try:
        if not vehicle_plate or zone_id not in ZONES:
            return None

        permit_no = "P" + str(random.randint(10000, 99999))
        expiry = datetime.now() + timedelta(days=180)
        permits[vehicle_plate] = {
            "zone": zone_id,
            "permit": permit_no,
            "expiry": expiry.strftime("%Y-%m-%d"),
        }
        zone_records.append((vehicle_plate, zone_id))
        return permit_no
    except Exception:
        return None


def revoke_permit(vehicle_plate):
    """Revoke the parking permit of a vehicle."""
    try:
        del permits[vehicle_plate]
    except KeyError:
        pass


def is_expired(vehicle_plate):
    """Check whether the permit of a vehicle has expired."""
    try:
        expiry = datetime.strptime(
            permits[vehicle_plate]["expiry"], "%Y-%m-%d"
        )
        return expiry < datetime.now()
    except (KeyError, ValueError):
        return False


def scan_zone(zone_id, plates_seen):
    """Scan a zone and return list of vehicles that should not be parked there."""
    flagged = []
    for plate in plates_seen:
        if (
            plate not in permits
            or permits[plate]["zone"] != zone_id
            or is_expired(plate)
        ):
            flagged.append(plate)
    return flagged


def load_permit_database(file="permits.json"):
    """Load permits from a JSON file into the global permits dictionary."""
    global permits
    try:
        with open(file, "r", encoding="utf-8") as f:
            permits = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        permits = {}


def save_permit_database(file="permits.json"):
    """Save the current permits dictionary into a JSON file."""
    with open(file, "w", encoding="utf-8") as f:
        json.dump(permits, f, indent=2)


def set_expiry(vehicle_plate, date_text):
    """Manually set the expiry date of a vehicle's permit."""
    if vehicle_plate in permits:
        permits[vehicle_plate]["expiry"] = date_text


def main():
    """Main function to demonstrate the parking permit system."""
    load_permit_database()
    register_permit("KA01AB1234", "A")
    register_permit("KA05XY9999", "Z")   # invalid zone
    register_permit("", "B")             # empty plate
    register_permit(None, "C")           # None plate
    set_expiry("KA01AB1234", "01/01/2020")
    revoke_permit("MH12ZZ0000")
    print(
        "Flagged in zone A:",
        scan_zone("A", ["KA01AB1234", "KA05XY9999", "TN09QQ1111"]),
    )
    plate = input("Plate to revoke (Enter to skip): ")
    revoke_permit(plate)
    save_permit_database()
    print("Permits on file:", len(permits))


if __name__ == "__main__":
    main()

import os
import subprocess

BAT_PATH = "/proc/acpi/battery/BAT%d"


def get_full_charge(batt_path):
    """Get the max capacity of the battery
    :param batt_path: The dir path to the battery (acpi) processes
    :type batt_path: string
    :returns: The max capacity of the battery
    :rtype: int
    """
    p1 = subprocess.Popen(["grep",
                            "last full capacity",
                            batt_path + "/info"],
                         stdout=subprocess.PIPE)
    p2 = subprocess.Popen(["awk",
                            "{print $4}"],
                            stdin=p1.stdout,
                            stdout=subprocess.PIPE)
    p1.stdout.close()
    return int(p2.communicate()[0])


def get_current_charge(batt_path):
    """Get the current capacity of the battery
    :param batt_path: The dir path to the battery (acpi) processes
    :type batt_path: string
    :returns: The current capacity of the battery
    :rtype: int
    """
    p1 = subprocess.Popen(["grep",
                            "remaining capacity",
                            batt_path + "/state"],
                         stdout=subprocess.PIPE)
    p2 = subprocess.Popen(["awk",
                            "{print $3}"],
                            stdin=p1.stdout,
                            stdout=subprocess.PIPE)
    p1.stdout.close()
    return int(p2.communicate()[0])


def guess_battery_path():
    """Gets the path of the battery (BAT0, BAT1...)
    :returns: The path to the battery acpi process information
    :rtype: string
    """

    i = 0
    while True:
        if os.path.exists(BAT_PATH % i):
            return BAT_PATH % i
        i += 1


def is_plugged(batt_path):
    """Returns a flag saying if the battery is plugged in or not
    :param batt_path: The dir path to the battery (acpi) processes
    :type batt_path: string
    :returns: A flag, true is plugged, false unplugged
    :rtype: bool
    """
    p = subprocess.Popen(["grep",
                            "charging state",
                            batt_path + "/state"],
                         stdout=subprocess.PIPE)
    return "discharging" not in p.communicate()[0]


def get_battery_percent(batt_path):
    """Calculates the percent of the battery based on the different data of
    the battery processes
    :param batt_path: The dir path to the battery (acpi) processes
    :type batt_path: string
    :returns: The percent translation of the battery total and current capacity
    :rtype: int
    """

    return get_current_charge(batt_path) * 100 / get_full_charge(batt_path)


def main():
    path = guess_battery_path()
    print("Current battery percent: %d" % get_battery_percent(path))
    print("Plugged in" if is_plugged(path) else "Not plugged in")

if __name__ == "__main__":
    main()
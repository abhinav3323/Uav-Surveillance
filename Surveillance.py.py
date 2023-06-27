from __future__ import print_function
import time
from dronekit import connect, VehicleMode, LocationGlobalRelative



# Set up option parsing to get connection string
import argparse
parser = argparse.ArgumentParser(description='Commands vehicle using vehicle.simple_goto.')
parser.add_argument('--connect',
                    help="Vehicle connection target string. If not specified, SITL automatically started and used.")
args = parser.parse_args()

connection_string = args.connect
sitl = None


# Start SITL if no connection string specified
if not connection_string:
    import dronekit_sitl
    sitl = dronekit_sitl.start_default()
    connection_string = sitl.connection_string()


# Connect to the Vehicle
print('Connecting to vehicle on: %s' % connection_string)
vehicle = connect(connection_string, wait_ready=True)


def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude)  # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto
    #  (otherwise the command after Vehicle.simple_takeoff will execute
    #   immediately).
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        # Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)


arm_and_takeoff(10)

print("Set default/target airspeed to 3")
vehicle.airspeed = 3
x1,y1,x2,y2,step = 25.494649272356195, 81.86395831175112 , 25.49528029187625, 81.86549214750461, 10000
###########################################################################################################

no_of_steps = int((x2 - x1)/2*step)
for i in range(0, no_of_steps):
    point1 = LocationGlobalRelative(x2-i*step,y1+i*step, 10)
    print("movind to p1")
    vehicle.simple_goto(point1, groundspeed=10)
    time.sleep(10)
    print("movind to p2")
    point2 = LocationGlobalRelative(x2-i*step,y2-i*step, 10)
    vehicle.simple_goto(point2, groundspeed=10)
    time.sleep(10)
    print("movind to p1")
    point3 = LocationGlobalRelative(x1+i*step,y2-i*step, 10)
    vehicle.simple_goto(point3, groundspeed=10)
    time.sleep(10)
    print("movind to p1")
    point4 = LocationGlobalRelative(x1+i*step,y1+(i+1)*step, 10)
    vehicle.simple_goto(point4, groundspeed=10)
    time.sleep(10)
    print("movind to p1")
###########################################################################################################
print("Returning to Launch")
vehicle.mode = VehicleMode("RTL")

# Close vehicle object before exiting script
print("Close vehicle object")
vehicle.close()

# Shut down simulator if it was started.
if sitl:
    sitl.stop()

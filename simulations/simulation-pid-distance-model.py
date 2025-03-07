import sys, getopt
from src.platoon.platoon_bidirectional_pid_truck import PlatoonBidirectionalPidTruckS3, PlatoonBidirectionalPidTruckS1, PlatoonBidirectionalPidTruckS2
from src.platoon.platoon_pid_distance_truck import PlatoonPidDistanceTruckS1, PlatoonPidDistanceTruckS2, PlatoonPidDistanceTruckS3, PlatoonPidDistanceTruckS4
from src.platoon.platoon_pid_distance_rc_vehicle import PlatoonPidDistanceRcVehicleS1, PlatoonPidDistanceRcVehicleS2, PlatoonPidDistanceRcVehicleS3
from src.common.plot import plot_speed, plot_travel_distance, plot_distances, plot_position


def simulate(num_tick, num_vehicles, scenario, type, model):
    match (scenario, type, model):
        case (1,1,1):
            p = PlatoonPidDistanceTruckS1(num_vehicles)
            suffix = "pid-distance-model-s1-truck"
        case (2,1,1):
            p = PlatoonPidDistanceTruckS2(num_vehicles)
            suffix = "pid-distance-model-s2-truck"
        case (3,1,1):
            p = PlatoonPidDistanceTruckS3(num_vehicles)
            suffix = "pid-distance-model-s3-truck"
        case (4,1,1):
            p = PlatoonPidDistanceTruckS4(num_vehicles)
            suffix = "pid-distance-model-s4-truck"
        case (1,3,1):
            p = PlatoonPidDistanceRcVehicleS1(num_vehicles)
            suffix = "pid-distance-model-s1-rc-vehicle"
        case (2,3,1):
            p = PlatoonPidDistanceRcVehicleS2(num_vehicles)
            suffix = "pid-distance-model-s2-rc-vehicle"
        case (3,3,1):
            p = PlatoonPidDistanceRcVehicleS3(num_vehicles)
            suffix = "pid-distance-model-s3-rc-vehicle"
        case (1,1,2):
            p = PlatoonBidirectionalPidTruckS1(num_vehicles)
            suffix = "bidirectional-pid-model-s1-truck"
        case (2,1,2):
            p = PlatoonBidirectionalPidTruckS2(num_vehicles)
            suffix = "bidirectional-pid-model-s2-truck"
        case (3,1,2):
            p = PlatoonBidirectionalPidTruckS3(num_vehicles)
            suffix = "bidirectional-pid-model-s3-truck"
        case (_,_,_):
            print("Unknown option")
            exit(1)
    print(suffix)

    # Each tick is 10ms
    for tick in range(num_tick):
        p.run(tick)

    speeds = p.get_speeds()
    travel_distance = p.get_travel_distance()
    distances = p.get_distances()
    positions = p.get_positions()

    plot_speed(speeds, num_vehicles, f'plots/speeds-with-{suffix}.png')
    plot_travel_distance(travel_distance, num_vehicles, f'plots/travel-distance-with-{suffix}.png')
    plot_distances(distances, num_vehicles, f'plots/distances-with-{suffix}.png')
    plot_position(positions, num_vehicles, f'plots/positions-with-{suffix}.png')


def main(argv):
    num_ticks = 0
    num_vehicles = 0
    scenario = 1
    type = 1
    model = 1
    opts, args = getopt.getopt(argv,"ht:s:v:y:m:",["ticks=","scenario=","vehicles=","type=","model="])
    for opt, arg in opts:
        if opt == '-h':
            print ('simulation-pid-distance-model.py -t <number of ticks> -s <scenario> -v <number of vehicles> -y <vehicle type>')
            print ('Vehicle type:')
            print ('\t1: Truck')
            print ('\t2: DIY-kit vehicle (TODO)')
            print ('\t3: RC vehicle (TODO)')
            print ('Model to use:')
            print ('\t1: PID distance')
            print ('\t2: Bidirectional')
            sys.exit()
        elif opt in ("-t", "--ticks"):
            num_ticks = int(arg)
        elif opt in ("-s", "--scenario"):
            scenario = int(arg)
        elif opt in ("-v", "--vehicles"):
            num_vehicles = int(arg)
        elif opt in ("-y", "--type"):
            type = int(arg)
        elif opt in ("-m", "--model"):
            model = int(arg)

    simulate(num_ticks, num_vehicles, scenario, type, model)



if __name__ == "__main__":
    main(sys.argv[1:])

    # Examples
    #simulate(20000, 5, 1)
    #simulate(2000, 5, 2)
    #simulate(20000, 5, 3)

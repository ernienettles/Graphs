from room import Room
from player import Player
from world import World
from queue import Queue

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

def get_traversal_path():
    rooms = {}

    # Depth first traversal
    def dft(current_room, visited=None):
        # If the room has not been visited create an empty set
        if not visited:
            visited = set()
        # Otherwise return
        elif current_room.id in visited:
            return

        # Adds the current room id to the visited set
        visited.add(current_room.id)
        # Sets the current_room.id key as an empty object
        rooms[current_room.id] = {}
        # Gets all exits within the current room
        exits = current_room.get_exits()

        # Loops through the directions in exits
        for direction in exits:
            # Assigns neighbor to the room in the current direction
            neighbor = current_room.get_room_in_direction(direction)
            # Assigns the current room id key with an object containing direction keys with neighbor ids as values.
            rooms[current_room.id][direction] = neighbor.id
            # Recursively run the traversal again starting at the neighbor this time
            dft(neighbor, visited)


    # Breadth first search
    def bfs(starting_id, destination_id):
        # Creates a queue
        q = Queue()
        # Puts the item into the queue
        q.put([starting_id])
        # Creates an empty set for visited rooms
        visited = set()

        # Creates a while loop that runs if the queue is not empty
        while not q.empty():
            # This removes and returns an item from the queue
            path = q.get()
            # Sets the current_room_id to the last item in path
            current_room_id = path[-1]

            # If the room is in visited, continue
            if current_room_id in visited:
                continue
            
            # If the current_room_id equals the destination_id return the path
            if current_room_id == destination_id:
                return path
            # Adds the current room to visited
            visited.add(current_room_id)

            # Returns all values within the current_room_id dictionary then loops through them
            for room_id in rooms[current_room_id].values():
                q.put(path + [room_id])
    
    # Traverses the graph and fills rooms with directions and the ids of the rooms in those directions
    dft(player.current_room)
    # Grabs the room IDs
    ids = list(rooms.keys())

    traversal_path = []

    # Starts at the starting id and move up one with every iteration
    for i in range(len(ids) - 1):
        # Finds the path from the first id to the next
        path = bfs(ids[i], ids[i + 1])

        # Iterates througn the path, then appends every direction to traversal_path
        for j in range(len(path) - 1):
            cur_room_id, next_room_id = path[j], path[j + 1]
            for direction, room_id in rooms[cur_room_id].items():
                if room_id == next_room_id:
                    traversal_path.append(direction)

    return traversal_path

traversal_path = get_traversal_path()

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")

import pygame
import random

# Initialize Pygame
pygame.init()

# Define constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
LANE_HEIGHT = SCREEN_HEIGHT // 2
CAR_WIDTH = 35
CAR_HEIGHT = 20
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
FPS = 60  # Frames per second
TIME_BEFORE_YELLOW = 3  # Duration before switching to yellow
YELLOW_DURATION = 2  # Duration for yellow light
SPAWN_INTERVAL = 60  # Frames until the next vehicle is spawned

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Realistic Traffic Simulation")

# Vehicle class with lane switching and movement logic
class Vehicle:
    def __init__(self, id, speed, position, lane, max_speed, safe_distance=40, behavior="normal"):
        self.id = id
        self.speed = speed
        self.position = position
        self.lane = lane
        self.max_speed = max_speed
        self.safe_distance = safe_distance
        self.behavior = behavior  # "normal", "aggressive", "cautious"
        self.color = BLUE if self.lane == 0 else RED

    def move(self, time_step, road, traffic_lights):
        self.check_lane_change(road)  # Check for lane change
        self.adjust_speed(road, traffic_lights)  # Adjust speed based on traffic and lights
        self.position += self.speed * time_step  # Move vehicle

    def adjust_speed(self, road, traffic_lights):
        # Find the car directly ahead in the same lane
        car_ahead = road.find_car_ahead(self)

        # Check for nearby traffic lights
        for light in traffic_lights:
            if abs(self.position - light.position) < self.safe_distance:
                if light.is_green():
                    self.speed = min(self.speed, self.max_speed)  # Maintain speed
                elif light.is_yellow():
                    self.speed = min(self.speed, self.max_speed * 0.5)  # Reduce speed during yellow light
                else:
                    self.speed = 0  # Stop at red light
                    return
        
        # Maintain safe distance from the car ahead
        if car_ahead and car_ahead.position - self.position < self.safe_distance:
            # Decelerate to avoid collision
            self.speed = max(self.speed - 2, 0)
        else:
            # Accelerate based on driver behavior
            if self.behavior == "aggressive":
                self.speed = min(self.speed + 4, self.max_speed)  # Faster acceleration
            elif self.behavior == "cautious":
                self.speed = min(self.speed + 1, self.max_speed)  # Slower acceleration
            else:
                self.speed = min(self.speed + 2, self.max_speed)  # Normal acceleration

    def check_lane_change(self, road):
        car_ahead = road.find_car_ahead(self)
        if car_ahead and car_ahead.position - self.position < self.safe_distance:
            other_lane = 1 - self.lane  # Switch to the other lane
            if road.is_lane_clear(self, other_lane):
                self.lane = other_lane  # Change lane if it's clear

    def draw(self, screen):
        # Draw the vehicle as a rectangle
        x = self.position
        y = LANE_HEIGHT * self.lane + (LANE_HEIGHT - CAR_HEIGHT) // 2
        pygame.draw.rect(screen, self.color, (x, y, CAR_WIDTH, CAR_HEIGHT))

# Traffic Light class
class TrafficLight:
    def __init__(self, position, green_duration, red_duration):
        self.position = position  # Position of the light on the road
        self.green_duration = green_duration  # Duration of green light in seconds
        self.red_duration = red_duration  # Duration of red light in seconds
        self.yellow_duration = YELLOW_DURATION  # Duration of yellow light
        self.time = 0  # Current time in the cycle
        self.state = "green"  # Initial state of the light

    def update(self, time_step):
        self.time += time_step
        if self.state == "green" and self.time >= self.green_duration:
            self.state = "yellow"
            self.time = 0
        elif self.state == "yellow" and self.time >= self.yellow_duration:
            self.state = "red"
            self.time = 0
        elif self.state == "red" and self.time >= self.red_duration:
            self.state = "green"
            self.time = 0

    def is_green(self):
        return self.state == "green"
    
    def is_yellow(self):
        return self.state == "yellow"

    def draw(self, screen):
        color = (0, 255, 0) if self.state == "green" else (255, 0, 0) if self.state == "red" else YELLOW
        pygame.draw.circle(screen, color, (self.position, 50), 20)

# Road class to manage vehicles and simulate traffic
class Road:
    def __init__(self, num_lanes):
        self.num_lanes = num_lanes
        self.vehicles = []
        self.traffic_lights = []

    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)

    def add_traffic_light(self, light):
        self.traffic_lights.append(light)

    def find_car_ahead(self, vehicle):
        same_lane_cars = [v for v in self.vehicles if v.lane == vehicle.lane and v.position > vehicle.position]
        if same_lane_cars:
            return min(same_lane_cars, key=lambda v: v.position)  # Nearest car ahead
        return None

    def is_lane_clear(self, vehicle, lane):
        cars_in_lane = [v for v in self.vehicles if v.lane == lane]
        for car in cars_in_lane:
            if abs(car.position - vehicle.position) < vehicle.safe_distance:
                return False
        return True

    def simulate(self, time_step):
        # Update traffic lights
        for light in self.traffic_lights:
            light.update(time_step)
        
        # Move vehicles
        for vehicle in self.vehicles:
            vehicle.move(time_step, self, self.traffic_lights)

        # Remove vehicles that have moved off-screen
        self.vehicles = [v for v in self.vehicles if v.position < SCREEN_WIDTH]

    def draw(self, screen):
        pygame.draw.line(screen, BLACK, (0, LANE_HEIGHT), (SCREEN_WIDTH, LANE_HEIGHT), 5)
        for vehicle in self.vehicles:
            vehicle.draw(screen)
        for light in self.traffic_lights:
            light.draw(screen)

# Main loop
def main():
    # Initialize the road with lanes and traffic lights
    road = Road(num_lanes=2)
    
    # Variables for vehicle spawning
    clock = pygame.time.Clock()
    frame_count = 0  # Counter for spawning vehicles

    # Add traffic lights at specific positions
    road.add_traffic_light(TrafficLight(position=200, green_duration=5, red_duration=5))
    road.add_traffic_light(TrafficLight(position=400, green_duration=6, red_duration=4))

    running = True
    while running:
        screen.fill(WHITE)  # Clear the screen

        # Handle events (like quitting the game)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Increment frame count and spawn vehicles at intervals
        frame_count += 1
        if frame_count >= SPAWN_INTERVAL:
            # Random speed and position for new vehicle
            speed = random.randint(15, 30)  # Random speed for vehicles
            position = 0  # Start from the left edge
            lane = random.randint(0, 1)  # Random lane (0 or 1)
            behavior = random.choice(["normal", "aggressive", "cautious"])  # Random behavior

            # Ensure there's enough distance between vehicles
            if road.is_lane_clear(Vehicle(id=len(road.vehicles)+1, speed=speed, position=position, lane=lane, max_speed=50, behavior=behavior), lane):
                road.add_vehicle(Vehicle(id=len(road.vehicles)+1, speed=speed, position=position, lane=lane, max_speed=50, behavior=behavior))

            frame_count = 0  # Reset frame count after spawning

        # Simulate and draw the road, vehicles, and traffic lights
        road.simulate(time_step=1 / FPS)
        road.draw(screen)

        pygame.display.flip()  # Update the display
        clock.tick(FPS)  # Maintain FPS

    pygame.quit()

# Run the main loop
if __name__ == "__main__":
    main()
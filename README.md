# TFL Bus and Overground Arrival Display

This project provides a live display of bus and overground train arrivals using Transport for London's API. It utilizes Python along with various libraries for fetching data, image processing, and GUI display.

## Requirements

- Python 3.x
- Requests library (`pip install requests`)
- Pygame library (`pip install pygame`)
- PIL (Pillow) library (`pip install Pillow`)

## Usage

1. Clone the repository:

   ```bash
   git clone https://github.com/calder-c/tfl-api-arrivals-board.git
   cd tfl-api-arrivals-board
   ```

3. Run the application:

   ```bash
   python main.py <bus NAPTAN> <bus route> <bus direction (inbound, outbound)> <overground NAPTAN> <overground direction (inbound, outbound)> <check interval (secs)>
   ```

   Ensure you provide the required arguments correctly.
   You must provide all of these arguments for the code to run properly.

## Functionality

- The `writer` thread fetches bus and overground train arrivals from the TfL API and generates an image to display.
- The `reader` thread renders the generated image using Pygame for a graphical user interface.

## Contributing

Contributions are welcome! If you have any suggestions, improvements, or feature requests, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](license) file for details.

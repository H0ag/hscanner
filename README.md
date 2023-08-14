# Hscanner Documentation

## Introduction

Welcome to the documentation for Hscanner, a local network IP scanner developed 100% in Python by Hoag. Hscanner allows you to scan IP addresses on a local network based on the provided subnet mask. The script performs a comprehensive scan from 0 to 255 to find active hosts.

## Installation

To install Hscanner, follow these simple steps:

1. Clone the Hscanner GitHub repository:

    ```shell
    git clone https://github.com/hoag/hscanner.git
    ```
    
2. Navigate to the project directory:
    ```shell
    cd Hscanner
    ```

3. Install the required dependencies using pip:

    ```shell
    pip install -r requirements.txt
    ```

## Usage
To use Hscanner, run the following command:
```shell
python hscanner.py
```
The script will guide you to enter the subnet mask. Once you've provided the mask, Hscanner will start scanning IP addresses from 0 to 255 within the local network and display the results.

## Custom Timeout
By default, Hscaner uses a timeout of 0.2 seconds between each ping. However, you can customize this timeout by using the ``-t`` flag followed by the desired timeout value in seconds. For example:

```shell
python hscaner.py -t 0.5
```
This will set the timeout to 0.5 seconds between pings.

## Example Usage
```shell
python Hscanner.py
```

Follow the prompts to enter the subnet mask. Afterward, Hscanner will begin scanning IP addresses and display results like this:

```
[+] <IP> Host is up <HOST>
```

## Author

- Hoag (https://double-t.fr/profiles/2a6a5c9b-8d78-4cc2-9cc4-c4c4d8fb3f4c)

![Hoag's profile picture](https://double-t.fr/ProfilesPictures/ProfilePicture_64c814e82e17e1.25709776.png "Hoag's profile picture")

Feel free to use this documentation, and don't hesitate to adapt it further to suit your exact needs. If you have any more questions or requests, feel free to ask!

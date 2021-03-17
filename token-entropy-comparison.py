"""
Save a number of generated values into a file.

This can be loaded into the Sequencer tool of Burp and analysed.
"""
import secrets


def save_to_file(filename, repeat):
    with open(filename, 'w') as f:
        for _ in range(repeat):
#            data = secrets.token_bytes(36)
#            data = secrets.token_hex(36)
            data = secrets.token_urlsafe(36)
            f.write(data)
            f.write('\n')


if __name__ == '__main__':
    save_to_file('secrets-token-urlsafe', 20000)

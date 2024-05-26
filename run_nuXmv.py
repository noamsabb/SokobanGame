import subprocess
import os


def run_nuxmv_interactive(model_filename):
    # Absolute path to the nuXmv executable
    nuxmv_path = "/Users/noam/Desktop/FormalVerification/Project/sokobanGame/nuXmv"  # Adjust this path if necessary

    # Create Output directory if it doesn't exist
    output_dir = "Output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")

    # Print the path to the nuXmv executable for debugging
    print(f"Checking if nuXmv executable exists at: {nuxmv_path}")

    # Ensure the nuXmv executable is found at the specified path
    if not os.path.isfile(nuxmv_path):
        raise FileNotFoundError(f"nuXmv executable not found at {nuxmv_path}")

    # Print message indicating the nuXmv executable was found
    print(f"nuXmv executable found at: {nuxmv_path}")

    # Start nuXmv in interactive mode
    nuxmv_process = subprocess.Popen(
        [nuxmv_path, "-int"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )

    # Define the commands to run
    commands = [
        f"read_model -i {model_filename}",
        "go",
        "check_ltlspec",
        "quit"
    ]
    # Join the commands into a single string with newline characters
    command_string = "\n".join(commands) + "\n"

    # Print the commands being sent to nuXmv for debugging
    print("Sending commands to nuXmv:")
    print(command_string)

    # Send the commands to nuXmv
    stdout, stderr = nuxmv_process.communicate(command_string)

    # Print output and error (if any)
    if stdout:
        print("nuXmv output:")
        print(stdout)
    if stderr:
        print("nuXmv errors:")
        print(stderr)

    # Save the output to a file
    output_filename = os.path.join(output_dir, os.path.basename(model_filename).split(".")[0] + ".out")
    with open(output_filename, "w") as f:
        f.write(stdout)


    print(f"Output saved to {output_filename}")

    return output_filename


# Example usage
model_filename = "example1.smv"  # Replace with your actual model filename
run_nuxmv_interactive(model_filename)

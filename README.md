# Accelerating python audio processing through rust bindings
This repository includes a basic exemplary implementation of a noise gate algorithm in both Python and Rust. An additional Python script invokes both implementations to compare their performance. The results indicate a notable speed advantage for the Rust implementation over the Python one. This suggests that integrating Rust into Python can be a practical strategy for audio processing, particularly in intricate pipelines like those encountered in training and computing inferences for machine learning models. In these scenarios, using Rust as an alternative can help cut costs, boost efficiency, and accelerate research outcomes and hypothesis validation.

The Python binding for the Rust code was generated using [`maturin`](https://github.com/PyO3/maturin) and [`pyo3`](https://github.com/PyO3/pyo3). Please check the respective repositories of these projects for further details.

The noise gate algorithm implements signal processing described [here](https://es.mathworks.com/help/audio/ref/noisegate.html).

# Structure of this repository
The repository contains two main folders described below:
- `python`: Python code consuming the Rust implementation of the noise gate and a Python-based implementation used to compare the performance of both. The comparison is performed in `main.py`, and the implementation details for each version of the noise gate is inside `noise_gate.py`.
- `rust`: Rust code implementing the noise gate function that is exported as a Python package.

# Installing and running the scripts
This repository assumes you have a working implementation of Rust. You can check Rust is correctly installed in your computer by typing `rustc --version` in the terminal and pressing enter, and you should the Rust compiler version. If you don't have Rust installed, please follow the instructions of the official Rust documentation [here](https://www.rust-lang.org/tools/install).

Once rust is installed, activate your Python environment and install the dependencies from the `requirements.txt` file by running:

```bash
python -m pip install -r requirements.txt
```

After the installation is finished, you should - among other dependencies - have now `maturin` installed. You can check this if you run:

```bash
maturin --version
```

If it prints `pymaturin x.y.z` where `x.y.z` is the version of `maturin`.
If this worked, then you are all set now. Congratulations!

The next step is to run `maturin`. This will compile the Rust code and also expose to your Python environment so you can import it in your project. To do this, go to the `rust` folder and run:

```bash
maturin develop --release
```

After everything is compiled correctly, you should see the following line in your terminal:
```
🛠 Installed noise-gate-rs-0.1.0
```

Now if you create a Python file, you should be able to import your package as follows:

```python
import noise_gate_rs
```

Now, to test both noise gate implementations, simply run the `main.py` script inside the `python` folder. This will process the same audio file `audio.wav` using both the Python and the Rust implementation. The performance of each implementation will be timed and printed to the console. To modify the parameters of each implementation, you can directly modify this script. An `audio_processed_py.wav` and `audio_processed_rs.wav` will be generated inside the `python` folder for you to listen to the end result.

# Measurements
These results are computed using the provided `audio.wav` audio file as reference.

| Python | Rust | Device                                  |
|--------|------|-----------------------------------------|
| 279ms  | 10ms | MacBook Pro M2 14-inch, 2023 (16GB RAM) |

# License
This project is licensed under the terms of the MIT license - see the [LICENSE](LICENSE) file for details.

import soundfile as sf
from time import perf_counter
from noise_gate import (
    NoiseGatePy,
    NoiseGateRs
)


def main():
    # Open audio file
    audio, fs = sf.read(file="audio.wav")

    # Instantiate noise gate (python)
    ng_py = NoiseGatePy(
        fs=fs,
        threshold_db=-40.0,
        attack_ms=20,
        sustain_ms=30,
        release_ms=80
    )

    # Instantiate noise gate (rust)
    ng_rs = NoiseGateRs(
        fs=fs,
        threshold_db=-40.0,
        attack_ms=20,
        sustain_ms=30,
        release_ms=80
    )

    # Process audio with the python implementation of the noise gate, save the
    # result and report the elapsed time
    py_start_time = perf_counter()
    processed_audio = ng_py(audio.copy())
    py_end_time = perf_counter()
    py_elapsed = py_end_time - py_start_time
    sf.write("audio_processed_rs.wav", processed_audio, samplerate=fs)
    print(f"NoiseGatePy: {(py_elapsed) * 1000.0} ms")

    # Process audio with the rust implementation of the noise gate, save the
    # result and report the elapsed time
    rs_start_time = perf_counter()
    processed_audio = ng_rs(audio.copy())
    rs_end_time = perf_counter()
    rs_elapsed = rs_end_time - rs_start_time
    sf.write("audio_processed_py.wav", processed_audio, samplerate=fs)
    print(f"NoiseGateRs: {(rs_elapsed) * 1000.0} ms")

    # Print difference as ratio
    if py_elapsed > rs_elapsed:
        ratio = py_elapsed / rs_elapsed
        print(f"NoiseGateRs was {ratio:2f} faster than NoiseGatePy")
    
    elif py_elapsed < rs_elapsed:
        ratio = rs_elapsed / py_elapsed
        print(f"NoiseGatePy was {ratio:2f} faster than NoiseGateRs")
    
    else:
        print("NoiseGateRs and NoiseGatePy have the same speed")


if __name__ == "__main__":
    main()

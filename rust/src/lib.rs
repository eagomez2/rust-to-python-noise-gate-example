use pyo3::prelude::*;


/// Apply a noise gate effect to a vector of audio samples.
///
/// # Arguments
///
/// * `samples` - A mutable vector of f32 representing the audio samples.
/// * `gc` - A mutable f32 representing the current gain computed value.
/// * `gs` - A mutable f32 representing the current gain smoothed.
/// * `sustain_count` - A mutable i32 representing the count of sustained samples.
/// * `threshold` - A f32 representing the threshold for activating the gate.
/// * `attack` - An i32 representing the attack time in samples
///     (Attack time is the time the applied gain takes to rise from 10% to 90%
///     of its final value when the input goes below the threshold).
/// * `sustain` - An i32 representing the sustain time in samples (sustain time
///     is the period for which the (negative) gain is held before starting to
///     decrease towards its steady state value when the input level drops
///     below the threshold).
/// * `release` - An i32 representing the release time in samples
///     (Release time is the time the applied gain takes to drop from 90% to
///     10% of its final value when the input goes above the threshold).
///
/// # Returns
///
/// A PyResult tuple containing:
/// * A mutable vector of f32 representing the modified audio samples.
/// * The updated gate computed value (`gc`).
/// * The updated gate smoothed value (`gs`).
/// * The updated count of sustained samples (`sustain_count`).
///
/// # Note
///
/// - All values should be in samples or linear amplitude.
/// - The function modifies the input `samples` vector in-place.
/// - Further details about the algorithm: https://es.mathworks.com/help/audio/ref/noisegate.html
#[pyfunction]
fn noise_gate(
    mut samples: Vec<f32>,
    mut gc: f32,
    mut gs: f32,
    mut sustain_count: i32,
    threshold: f32,
    attack: i32,
    sustain: i32,
    release: i32
) -> PyResult<(Vec<f32>, f32, f32, i32)> {
    // Calculate attack/release factors
    // -1.0 * 9.0_f32.ln(); 
    const FACTOR_NUM: f32 = -2.1972246;
    let attack_factor = (FACTOR_NUM * (attack as f32).recip()).exp();
    let release_factor = (FACTOR_NUM * (release as f32).recip()).exp();

    for sample in samples.iter_mut() {
        // Check if gate control is 0, reset sustain count
        if sample.abs() >= threshold {
            if gc == 0.0 {
                sustain_count = 0;
            }

            gc = 1.0;

        } else {
            // Increment sustain count and set gate control to 0
            sustain_count += 1;
            gc = 0.0;
        }

        // Adjust gate state based on sustain count, gc, and attack/release factors
        if sustain_count > sustain && gc <= gs {
            gs = attack_factor * gs + (1.0 - attack_factor) * gc; 

        }
        else if sustain_count <= sustain && gc > gs {
            gs = release_factor * gs + (1.0 - release_factor) * gc;
        }

        // Apply gate state to the current sample
        *sample *= gs;
    }

    Ok((samples, gc, gs, sustain_count))
}

/// A Python module implemented in Rust.
#[pymodule]
fn noise_gate_rs(_py: Python, m: &PyModule) -> PyResult<()> {
    // Add function to be callable form python
    m.add_function(wrap_pyfunction!(noise_gate, m)?)?;
    Ok(())
}

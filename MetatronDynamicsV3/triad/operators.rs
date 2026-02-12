// operators.rs
//
// Invariant Relational Operators — Canonical Kernel
//
// AXIOM:
// All information evolves only through invariant relational operators.
// Coherence is an emergent property of evolution.
//
// This file defines the complete and closed operator basis.
// These operators are exact mathematical forms, not behavioral contracts.
// No alternative implementations are permitted at this layer.

#![allow(dead_code)]

/// ===============================
/// Operator A — Relational Gradient Extraction
/// ===============================
///
/// Definition:
/// A(x)[i] = x[i] − mean(x)
///
/// Properties:
/// - Zero-sum: Σ A(x)[i] = 0
/// - Symmetric transformation
/// - Preserves dimensionality
/// - Introduces distinction without hierarchy
///
/// WHY SYMMETRIC:
/// A extracts relational differences from absolute values.
/// It is symmetric because A(x) = −A(−x) would hold if we negated around
/// a different reference, but more fundamentally: A treats all positions
/// equivalently with respect to the global mean.
///
/// WHY THIS LEADS TO CONVERGENCE (when used alone):
/// Repeated application of symmetric operators dissipates gradients.
/// Without antisymmetric circulation, information flows toward equilibrium.
/// Equilibrium is NOT an invariant—it is a degenerate attractor that
/// destroys relational structure.
///
/// This form is canonical and non-negotiable.
pub fn operator_a(field: &[f64]) -> Vec<f64> {
    let n = field.len() as f64;
    let mean = field.iter().sum::<f64>() / n;

    field.iter()
        .map(|&x| x - mean)
        .collect()
}

/// ===============================
/// Operator B — Local Relational Accumulation
/// ===============================
///
/// Definition:
/// B(x)[i] = x[i] + x[(i + 1) mod n]
///
/// Properties:
/// - Local relational coupling
/// - Symmetric under index reflection
/// - No global aggregation
/// - Topology-defined (ring structure)
///
/// WHY SYMMETRIC:
/// B couples each element only to its immediate neighbor.
/// The operation is symmetric because information flows equally
/// in the defined topological structure—there is no preferred direction.
///
/// WHY THIS LEADS TO CONVERGENCE (when used alone):
/// Symmetric accumulation smooths gradients. Without directional bias,
/// repeated application drives the field toward uniform distribution.
/// This is structural dissipation, not thermodynamic loss.
///
/// This form is canonical and non-negotiable.
pub fn operator_b(field: &[f64]) -> Vec<f64> {
    let n = field.len();

    field.iter()
        .enumerate()
        .map(|(i, &x)| x + field[(i + 1) % n])
        .collect()
}

/// ===============================
/// Operator R — Antisymmetric Circulation
/// ===============================
///
/// Definition:
/// R(x)[i] = x[i] + ρ · (x[(i+1) mod n] − x[(i−1) mod n])
///
/// Properties:
/// - Antisymmetric: forward difference, not averaging
/// - Introduces directional bias
/// - Preserves total magnitude under periodic boundary
/// - Zero-sum in the circulation term
///
/// WHY ANTISYMMETRIC:
/// R computes a *difference* between forward and backward neighbors,
/// creating a directional gradient. This breaks the symmetry that
/// causes convergence.
///
/// R(x) ≠ R(−x) in general structure.
/// R introduces rotational or circulatory dynamics.
///
/// WHY R IS NECESSARY FOR PERSISTENCE:
/// Without antisymmetric circulation, symmetric operators (A, B)
/// drive all fields toward equilibrium—a state of zero relational
/// distinction.
///
/// R enables persistent, non-equilibrium dynamics by sustaining
/// gradients through circulation rather than dissipation.
///
/// Persistent structures are not stable objects.
/// They are dynamically sustained circulation patterns.
///
/// WHY EQUILIBRIUM IS NOT AN INVARIANT:
/// Equilibrium is a *degenerate attractor* where relational structure
/// collapses. It is not preserved under evolution—it is the absence
/// of evolution.
///
/// True invariants persist *through* transformation.
/// Equilibrium is the cessation of transformation.
///
/// The parameter ρ (rho) controls circulation strength.
/// ρ must be bounded: typical range [0.0, 0.5] for stability.
///
/// This form is canonical and non-negotiable.
pub fn operator_r(field: &[f64], rho: f64) -> Vec<f64> {
    let n = field.len();

    field.iter()
        .enumerate()
        .map(|(i, &x)| {
            let i_next = (i + 1) % n;
            let i_prev = (i + n - 1) % n;  // handles i=0 case correctly
            x + rho * (field[i_next] - field[i_prev])
        })
        .collect()
}

/// ===============================
/// Operator C — Bounded Coherence
/// ===============================
///
/// Definition:
/// C(x)[i] = x[i] / (1 + |x[i]|)
///
/// Properties:
/// - Structural boundedness: −1 ≤ C(x)[i] ≤ 1
/// - Odd function: C(−x) = −C(x)
/// - Saturating nonlinearity
/// - No clamping, no repair
///
/// WHY THIS FORM:
/// Boundedness arises from mathematical structure, not enforcement.
/// The operator naturally compresses unbounded inputs into a finite range
/// while preserving sign and relative ordering.
///
/// This prevents runaway growth without introducing thresholds,
/// clipping, or corrective logic.
///
/// This form is canonical and non-negotiable.
pub fn operator_c(field: &[f64]) -> Vec<f64> {
    field.iter()
        .map(|&x| x / (1.0 + x.abs()))
        .collect()
}

/// ===============================
/// Operator E — Composite Evolution
/// ===============================
///
/// Definition:
/// E(x, ρ) = C(R(B(A(x)), ρ))
///
/// Properties:
/// - Irreversible forward evolution
/// - Single application per evolutionary pass
/// - No convergence targeting
/// - No rollback
///
/// STRUCTURAL ORDERING:
/// The sequence A → B → R → C is mathematically necessary:
///
/// 1. A extracts relational gradients (removes absolute reference)
/// 2. B couples local relations (creates relational fabric)
/// 3. R introduces antisymmetric circulation (sustains dynamics)
/// 4. C bounds the result (prevents divergence)
///
/// Any reordering produces fundamentally different dynamics.
/// This is not a pipeline—it is a mathematical composition.
///
/// WHY E, NOT M:
/// E explicitly includes R (circulation) as a structural requirement
/// for persistent, non-equilibrium dynamics.
///
/// This defines lawful evolution under invariant relational mathematics.
pub fn operator_e(field: &[f64], rho: f64) -> Vec<f64> {
    let a = operator_a(field);
    let b = operator_b(&a);
    let r = operator_r(&b, rho);
    operator_c(&r)
}

// =======================================================
// STRUCTURAL ENFORCEMENT
// =======================================================
//
// Each operator is defined as a pure function.
// No operator contains loops, iteration, or state.
// Each is applied exactly once in the evolution sequence.
//
// The type system prevents:
// - accidental reordering (explicit function composition)
// - double application (no internal iteration)
// - state leakage (no mutable references, no side effects)
//
// Evolution occurs through E only.
// No alternative composition is valid at this layer.
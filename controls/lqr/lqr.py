"""Author: Brandon Trabucco, Copyright 2019, MIT License"""


from controls.lqr.body import lqr_body
from controls.lqr.condition import lqr_condition
import tensorflow as tf


def lqr(
        dynamics_state_jacobian,
        dynamics_controls_jacobian,
        dynamics_shift,
        cost_state_state_hessian,
        cost_state_controls_hessian,
        cost_controls_state_hessian,
        cost_controls_controls_hessian,
        cost_state_jacobian,
        cost_controls_jacobian,
):
    """Solves for the value iteration solution to lqr.

    Args:
    - dynamics_state_jacobian: the jacobian of the dynamics wrt. state i
        with shape [T, batch_dim, ..., state_dim, state_dim].
    - dynamics_controls_jacobian: the jacobian of the dynamics wrt. controls i
        with shape [T, batch_dim, ..., state_dim, controls_dim].

    - dynamics_shift: the shift term of the dynamics
        with shape [T, batch_dim, ..., state_dim, 1].

    - cost_state_state_hessian: the hessian of the cost wrt. state i state j
        with shape [T, batch_dim, ..., state_dim, state_dim].
    - cost_state_controls_hessian: the hessian of the cost wrt. state i controls j
        with shape [T, batch_dim, ..., state_dim, controls_dim].
    - cost_controls_state_hessian: the hessian of the cost wrt. controls i state j
        with shape [T, batch_dim, ..., controls_dim, state_dim].
    - cost_controls_controls_hessian: the hessian of the cost wrt. controls i controls j
        with shape [T, batch_dim, ..., controls_dim, controls_dim].

    - cost_state_jacobian: the jacobian of the cost wrt. state i
        with shape [T, batch_dim, ..., state_dim, 1].
    - cost_controls_jacobian: the jacobian of the cost wrt. controls i
        with shape [T, batch_dim, ..., controls_dim, 1].

    Returns:
    - controls_state_jacobian: the jacobian of the controls with respect to the state
        with shape [T, batch_dim, ..., controls_dim, state_dim].
    - controls_shift: the shift term of the controls
        with shape [T, batch_dim, ..., controls_dim, 1].

    - value_state_state_hessian: the hessian of the cost to go wrt. state i state j
        with shape [T, batch_dim, ..., state_dim, state_dim].
    - value_state_jacobian: the jacobian of the cost to go wrt. state i
        with shape [T, batch_dim, ..., state_dim, 1].
        """

    # get the batch shape and vector sizes

    horizon = tf.shape(dynamics_state_jacobian)[0]

    batch_shape = tf.shape(dynamics_state_jacobian)[1:-2]

    batch_dim = tf.reduce_prod(batch_shape)

    state_dim = tf.shape(dynamics_state_jacobian)[-1]

    controls_dim = tf.shape(dynamics_controls_jacobian)[-1]

    dtype = dynamics_controls_jacobian.dtype

    # check the horizon of every tensor

    tf.debugging.assert_equal(
        horizon,
        tf.shape(dynamics_state_jacobian)[0],
        message="dynamics_state_jacobian should have correct horizon")

    tf.debugging.assert_equal(
        horizon,
        tf.shape(dynamics_controls_jacobian)[0],
        message="dynamics_controls_jacobian should have correct horizon")

    tf.debugging.assert_equal(
        horizon,
        tf.shape(dynamics_shift)[0],
        message="dynamics_shift should have correct horizon")

    tf.debugging.assert_equal(
        horizon,
        tf.shape(cost_state_state_hessian)[0],
        message="cost_state_state_hessian should have correct horizon")

    tf.debugging.assert_equal(
        horizon,
        tf.shape(cost_state_controls_hessian)[0],
        message="cost_state_controls_hessian should have correct horizon")

    tf.debugging.assert_equal(
        horizon,
        tf.shape(cost_controls_state_hessian)[0],
        message="cost_controls_state_hessian should have correct horizon")

    tf.debugging.assert_equal(
        horizon,
        tf.shape(cost_controls_controls_hessian)[0],
        message="cost_controls_controls_hessian should have correct horizon")

    tf.debugging.assert_equal(
        horizon,
        tf.shape(cost_state_jacobian)[0],
        message="cost_state_jacobian should have correct horizon")

    tf.debugging.assert_equal(
        horizon,
        tf.shape(cost_controls_jacobian)[0],
        message="cost_controls_jacobian should have correct horizon")

    # make sure all inputs have the same batch shape

    tf.debugging.assert_equal(
        batch_shape,
        tf.shape(dynamics_state_jacobian)[1:-2],
        message="dynamics_state_jacobian should have correct batch shape")

    tf.debugging.assert_equal(
        batch_shape,
        tf.shape(dynamics_controls_jacobian)[1:-2],
        message="dynamics_controls_jacobian should have correct batch shape")

    tf.debugging.assert_equal(
        batch_shape,
        tf.shape(dynamics_shift)[1:-2],
        message="dynamics_shift should have correct batch shape")

    tf.debugging.assert_equal(
        batch_shape,
        tf.shape(cost_state_state_hessian)[1:-2],
        message="cost_state_state_hessian should have correct batch shape")

    tf.debugging.assert_equal(
        batch_shape,
        tf.shape(cost_state_controls_hessian)[1:-2],
        message="cost_state_controls_hessian should have correct batch shape")

    tf.debugging.assert_equal(
        batch_shape,
        tf.shape(cost_controls_state_hessian)[1:-2],
        message="cost_controls_state_hessian should have correct batch shape")

    tf.debugging.assert_equal(
        batch_shape,
        tf.shape(cost_controls_controls_hessian)[1:-2],
        message="cost_controls_controls_hessian should have correct batch shape")

    tf.debugging.assert_equal(
        batch_shape,
        tf.shape(cost_state_jacobian)[1:-2],
        message="cost_state_jacobian should have correct batch shape")

    tf.debugging.assert_equal(
        batch_shape,
        tf.shape(cost_controls_jacobian)[1:-2],
        message="cost_controls_jacobian should have correct batch shape")

    # make sure all other dims are as expected

    tf.debugging.assert_equal(
        state_dim,
        tf.shape(dynamics_state_jacobian)[-2],
        message="dynamics_state_jacobian should have shape [T, batch_dim, ..., state_dim, state_dim]")

    tf.debugging.assert_equal(
        state_dim,
        tf.shape(dynamics_state_jacobian)[-1],
        message="dynamics_state_jacobian should have shape [T, batch_dim, ..., state_dim, state_dim]")

    tf.debugging.assert_equal(
        state_dim,
        tf.shape(dynamics_controls_jacobian)[-2],
        message="dynamics_controls_jacobian should have shape [T, batch_dim, ..., state_dim, controls_dim]")

    tf.debugging.assert_equal(
        controls_dim,
        tf.shape(dynamics_controls_jacobian)[-1],
        message="dynamics_controls_jacobian should have shape [T, batch_dim, ..., state_dim, controls_dim]")

    tf.debugging.assert_equal(
        state_dim,
        tf.shape(dynamics_shift)[-2],
        message="dynamics_shift should have shape [T, batch_dim, ..., state_dim, 1]")

    tf.debugging.assert_equal(
        1,
        tf.shape(dynamics_shift)[-1],
        message="dynamics_shift should have shape [T, batch_dim, ..., state_dim, 1]")

    tf.debugging.assert_equal(
        state_dim,
        tf.shape(cost_state_state_hessian)[-2],
        message="cost_state_state_hessian should have shape [T, batch_dim, ..., state_dim, state_dim]")

    tf.debugging.assert_equal(
        state_dim,
        tf.shape(cost_state_state_hessian)[-1],
        message="cost_state_state_hessian should have shape [T, batch_dim, ..., state_dim, state_dim]")

    tf.debugging.assert_equal(
        state_dim,
        tf.shape(cost_state_controls_hessian)[-2],
        message="cost_state_controls_hessian should have shape [T, batch_dim, ..., state_dim, controls_dim]")

    tf.debugging.assert_equal(
        controls_dim,
        tf.shape(cost_state_controls_hessian)[-1],
        message="cost_state_controls_hessian should have shape [T, batch_dim, ..., state_dim, controls_dim]")

    tf.debugging.assert_equal(
        controls_dim,
        tf.shape(cost_controls_state_hessian)[-2],
        message="cost_controls_state_hessian should have shape [T, batch_dim, ..., controls_dim, state_dim]")

    tf.debugging.assert_equal(
        state_dim,
        tf.shape(cost_controls_state_hessian)[-1],
        message="cost_controls_state_hessian should have shape [T, batch_dim, ..., controls_dim, state_dim]")

    tf.debugging.assert_equal(
        controls_dim,
        tf.shape(cost_controls_controls_hessian)[-2],
        message="cost_controls_controls_hessian should have shape [T, batch_dim, ..., controls_dim, controls_dim]")

    tf.debugging.assert_equal(
        controls_dim,
        tf.shape(cost_controls_controls_hessian)[-1],
        message="cost_controls_controls_hessian should have shape [T, batch_dim, ..., controls_dim, controls_dim]")

    tf.debugging.assert_equal(
        state_dim,
        tf.shape(cost_state_jacobian)[-2],
        message="cost_state_jacobian should have shape [T, batch_dim, ..., state_dim, 1]")

    tf.debugging.assert_equal(
        1,
        tf.shape(cost_state_jacobian)[-1],
        message="cost_state_jacobian should have shape [T, batch_dim, ..., state_dim, 1]")

    tf.debugging.assert_equal(
        controls_dim,
        tf.shape(cost_controls_jacobian)[-2],
        message="cost_controls_jacobian should have shape [T, batch_dim, ..., controls_dim, 1]")

    tf.debugging.assert_equal(
        1,
        tf.shape(cost_controls_jacobian)[-1],
        message="cost_controls_jacobian should have shape [T, batch_dim, ..., controls_dim, 1]")

    # flatten the batch shape of every tensor

    dynamics_state_jacobian = tf.reshape(
        dynamics_state_jacobian, [horizon, batch_dim, state_dim, state_dim])

    dynamics_controls_jacobian = tf.reshape(
        dynamics_controls_jacobian, [horizon, batch_dim, state_dim, controls_dim])

    dynamics_shift = tf.reshape(
        dynamics_shift, [horizon, batch_dim, state_dim, 1])

    cost_state_state_hessian = tf.reshape(
        cost_state_state_hessian, [horizon, batch_dim, state_dim, state_dim])

    cost_state_controls_hessian = tf.reshape(
        cost_state_controls_hessian, [horizon, batch_dim, state_dim, controls_dim])

    cost_controls_state_hessian = tf.reshape(
        cost_controls_state_hessian, [horizon, batch_dim, controls_dim, state_dim])

    cost_controls_controls_hessian = tf.reshape(
        cost_controls_controls_hessian, [horizon, batch_dim, controls_dim, controls_dim])

    cost_state_jacobian = tf.reshape(
        cost_state_jacobian, [horizon, batch_dim, state_dim, 1])

    cost_controls_jacobian = tf.reshape(
        cost_controls_jacobian, [horizon, batch_dim, controls_dim, 1])

    # create the loop variables

    initial_controls_state_jacobian = tf.zeros(
        [batch_dim, controls_dim, state_dim], dtype=dtype)

    initial_controls_shift = tf.zeros(
        [batch_dim, controls_dim, 1], dtype=dtype)

    initial_value_state_state_hessian = tf.zeros(
        [batch_dim, state_dim, state_dim], dtype=dtype)

    initial_value_state_jacobian = tf.zeros(
        [batch_dim, state_dim, 1], dtype=dtype)

    controls_state_jacobian_array = tf.TensorArray(dtype, size=horizon)

    controls_shift_array = tf.TensorArray(dtype, size=horizon)

    value_state_state_hessian_array = tf.TensorArray(dtype, size=horizon)

    value_state_jacobian_array = tf.TensorArray(dtype, size=horizon)

    time = horizon - 1

    # run the planner forward through time

    lqr_results = tf.while_loop(
        lqr_condition,
        lqr_body, (
            initial_controls_state_jacobian,
            initial_controls_shift,
            initial_value_state_state_hessian,
            initial_value_state_jacobian,
            dynamics_state_jacobian,
            dynamics_controls_jacobian,
            dynamics_shift,
            cost_state_state_hessian,
            cost_state_controls_hessian,
            cost_controls_state_hessian,
            cost_controls_controls_hessian,
            cost_state_jacobian,
            cost_controls_jacobian,
            controls_state_jacobian_array,
            controls_shift_array,
            value_state_state_hessian_array,
            value_state_jacobian_array,
            time,
            horizon))

    # collect the outputs and make sure they are the correct shape

    controls_state_jacobian = tf.reshape(
        lqr_results[13].stack(),
        tf.concat([[horizon], batch_shape, [controls_dim, state_dim]], 0))

    controls_shift = tf.reshape(
        lqr_results[14].stack(),
        tf.concat([[horizon], batch_shape, [controls_dim, 1]], 0))

    value_state_state_hessian = tf.reshape(
        lqr_results[15].stack(),
        tf.concat([[horizon], batch_shape, [state_dim, state_dim]], 0))

    value_state_jacobian = tf.reshape(
        lqr_results[16].stack(),
        tf.concat([[horizon], batch_shape, [state_dim, 1]], 0))

    return (
        controls_state_jacobian,
        controls_shift,
        value_state_state_hessian,
        value_state_jacobian)

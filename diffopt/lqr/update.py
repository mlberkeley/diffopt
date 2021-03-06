"""Author: Brandon Trabucco, Copyright 2019, MIT License"""


import tensorflow as tf


def update(
        Vxx,
        Vx,
        Fx,
        Fu,
        Cxx,
        Cxu,
        Cux,
        Cuu,
        Cx,
        Cu,
):
    """Solves for the value iteration solution to lqr.

    Args:
    - Vxx: the hessian of the cost to go wrt. state i state j
        with shape [batch_dim, state_dim, state_dim].
    - Vx: the jacobian of the cost to go wrt. state i
        with shape [batch_dim, state_dim, 1].

    - Fx: the jacobian of the dynamics wrt. state i
        with shape [batch_dim, state_dim, state_dim].
    - Fu: the jacobian of the dynamics wrt. controls i
        with shape [batch_dim, state_dim, controls_dim].

    - Cxx: the hessian of the cost wrt. state i state j
        with shape [batch_dim, state_dim, state_dim].
    - Cxu: the hessian of the cost wrt. state i controls j
        with shape [batch_dim, state_dim, controls_dim].
    - Cux: the hessian of the cost wrt. controls i state j
        with shape [batch_dim, controls_dim, state_dim].
    - Cuu: the hessian of the cost wrt. controls i controls j
        with shape [batch_dim, controls_dim, controls_dim].

    - Cx: the jacobian of the cost wrt. state i
        with shape [batch_dim, state_dim, 1].
    - Cu: the jacobian of the cost wrt. controls i
        with shape [batch_dim, controls_dim, 1].

    Returns:
    - Qxx: the hessian of the cost to go wrt. state i state j
        with shape [batch_dim, state_dim, state_dim].
    - Qxu: the hessian of the cost to go wrt. state i controls j
        with shape [batch_dim, state_dim, controls_dim].
    - Qux: the hessian of the cost to go wrt. controls i state j
        with shape [batch_dim, controls_dim, state_dim].
    - Quu: the hessian of the cost to go wrt. controls i controls j
        with shape [batch_dim, controls_dim, controls_dim].

    - Qx: the jacobian of the cost to go wrt. state i
        with shape [batch_dim, state_dim, 1].
    - Qu: the jacobian of the cost to go wrt. controls i
        with shape [batch_dim, controls_dim, 1].

    - Kx: the jacobian of the diffopt with respect to the state
        with shape [batch_dim, controls_dim, state_dim].
    - k: the shift term of the diffopt
        with shape [batch_dim, controls_dim, 1].
    - S: covariance of the maximum entropy controls
        with shape [batch_dim, controls_dim, controls_dim].

    - Vxx: the hessian of the cost to go wrt. state i state j
        with shape [batch_dim, state_dim, state_dim].
    - Vx: the jacobian of the cost to go wrt. state i
        with shape [batch_dim, state_dim, 1].
    """
    FxVxx = tf.matmul(Fx, Vxx, transpose_a=True)
    FuVxx = tf.matmul(Fu, Vxx, transpose_a=True)

    Qxx = Cxx + tf.matmul(FxVxx, Fx)
    Qxu = Cxu + tf.matmul(FxVxx, Fu)
    Qux = Cux + tf.matmul(FuVxx, Fx)
    Quu = Cuu + tf.matmul(FuVxx, Fu)
    Qx = Cx + tf.matmul(Fx, Vx, transpose_a=True)
    Qu = Cu + tf.matmul(Fu, Vx, transpose_a=True)

    S = tf.linalg.inv(Quu)
    Kx = -tf.matmul(S, Qux)
    k = -tf.matmul(S, Qu)
    KxQuu = tf.matmul(Kx, Quu, transpose_a=True)

    Vxx = Qxx + tf.matmul(Qxu, Kx) + tf.matmul(Kx, Qux, transpose_a=True) + tf.matmul(KxQuu, Kx)
    Vx = Qx + tf.matmul(Qxu, k) + tf.matmul(Kx, Qu, transpose_a=True) + tf.matmul(KxQuu, k)
    return (
        Qxx,
        Qxu,
        Qux,
        Quu,
        Qx,
        Qu,
        Kx,
        k,
        S,
        Vxx,
        Vx)

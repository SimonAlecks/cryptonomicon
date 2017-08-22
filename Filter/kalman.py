# Recursion, fam:
#http://www.bzarg.com/p/how-a-kalman-filter-works-in-pictures/
# Increment and go to step 1.
import numpy as np
from numpy.linalg import inv
import pandas as pd
import matplotlib.pyplot as plt

class Kalman():

    """
    x_{t+1} = A x_t + w_{t+1}       (w_t ~ N(0, Q))
    y_t = G x_t + v_t               (v_t ~ N(0, R))
    
    * A is n x n -- State Transition Matrix
    
    * Q is n x n, symmetric and nonnegative definite
    * w_t -- Process noise
    
    * G is k x n -- Observation Matrix
    * v_t -- Observation noise
    * R is k x k, symmetric and nonnegative definite
    """

    def __init__(self, y, x_h, s, G, R, A, Q):

        # Set Prior
        self.x_prior, self.s_prior = x_h, s

        # Set State Matrices
        self.y = y
        self.A, self.G, self.Q, self.R = map(self.convert, (A, G, Q, R))
        self.k, self.n = self.G.shape
        self.T = len(y)

        # Set Index and Output Data.
        self.output_data = pd.DataFrame(data=np.nan, index=self.y.index, columns=['filtered_state', 'one_step_ahead'])

    @staticmethod
    def convert(x):
        return np.atleast_2d(np.asarray(x, dtype='float32'))

    def run(self):

        y = self.y
        x, s = self.x_prior, self.s_prior

        for t, d in enumerate(self.y.index):
            y_v = np.atleast_2d(y.loc[d])
            x_, s_ = self._update_equation(x, s, y_v, d)
            x, s = self._prediction_equation(x_, s_, d)

    def _predict(self):
        pass

    def real_time_viz(self):

        plt.figure(1)
        plt.subplot(211)
        plt.plot(self.y)

    def _viz_update(self):
        plt.subplot(212)
        plt.plot(self.one_step_ahead_prediction)
        plt.show()

    def _update_equation(self, x, s, y, d):
        self._store_state(x, s, d)
        if np.isnan(y):
            return x, s
        # x_hat^F = x_hat + Sigma G' (G Sigma G' + R)^{-1}(y - G x_hat)
        # Sigma^F = Sigma - Sigma G' (G Sigma G' + R)^{-1} G Sigma

        G, R = self.G, self.R

        # x is the previous prediction of the state. We now observe a (noisy) y[t]. Combine information
        # Our prediction had noise, but so does our observation. What is the variance of our new signal?

        # Innovation or measurement pre-fit residual
        yk = (y - G * x)

        # Innovation of pre-fit covariance
        sk = G * s * G.T + R

        # Kalman gain is the matrix of population regression coefficients of the state x-x_hat
        # on the surprise y-Gx_hat
        K = s * G.T * inv(sk)

        # The new state is the prior state with the Kalman Gain multiplied by the implied state of the new observation
        # The combination between the two is based on the Kalman Gain. If R, which
        # is the covariance matrix of the state equation, is bigger the Kalman Gain is smaller, which means
        # We place less emphasis on the new observation. If the state variance-covariance is tiny, then we
        # trust the new measurement as probably-true.
        x_hatF = x + K * yk
        sigmaF = s - K * G * s

        # post-fit residual
        yk_k = (y - G * x_hatF)

        return x_hatF, sigmaF

    def _prediction_equation(self, x_, s_, d):
        self._store_one_step_ahead_prediction(x_, s_, d)

        # Predicted (a priori) state estimate
        x_ = self.A * x_
        # Predicted (a priori) estimate covariance
        s_ = self.A * s_ * self.A.transpose() + self.Q
        return x_, s_

    def _store_state(self, x, s, d):
        self.output_data.loc[d , 'filtered_state'] = x

    def _store_one_step_ahead_prediction(self, x_, s_, d):
        self.output_data.loc[d, 'one_step_ahead'] = x_


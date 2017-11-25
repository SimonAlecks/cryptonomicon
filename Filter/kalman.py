# Recursion, fam:
#http://www.bzarg.com/p/how-a-kalman-filter-works-in-pictures/
# Increment and go to step 1.
import numpy as np
from numpy.linalg import inv
import pandas as pd
import matplotlib.pyplot as plt

class Kalman():

    """

    y_t = Z_t*a_t + d_t + e_t             (e_t ~ N(0, H_t)
    a_t = T_t * a_t-1 + ct + R_t * n_t     (n_t ~ N(0, Q_t)
    
    * Z: design (k_endog x k_states x nobs)
    * d: obs intercept
    * H: observation covariance (k_endog * k_endog * nobs)
    * T: Transition (k_states * k_states * nobs)
    * c: State intercept (k_states x nobs)
    * R: Selection (k_states * k_posdef * nobs)
    * Q: state covariance (k_posdef x k_posdef x nobs)
    
    # Get states
    z_k_endog, z_k_state = Z.shape
    H_k_endog = H.shape[0]
    T_k_state = T.shape[0]
    R_k_posdef = R.shape[0]
    Q_k_posdef = Q.shape[0]

   
    """

    def __init__(self, a_h=0, s=0, y=None, T=None, H=None, Z=None, Q=None, R=None):

        # Set Prior
        self.a_prior, self.s_prior = a_h, s

        # Set State Matrices
        self.y = y
        # Design, Transition, State covariance, Observation covariance
        self.Z, self.T, self.Q, self.H, self.R = map(self.convert, (Z, T, Q, H, R))

        # Set Index and Output Data.
        self.output_data = pd.DataFrame(data=np.nan, index=self.y.index, columns=['filtered_state', 'one_step_ahead'])
        self.output_prediction = []
        self.output_data_list = []

    @staticmethod
    def convert(x):
        return np.atleast_2d(np.asarray(x, dtype='float32'))

    def _validate(self):
        n_a, n_a =np.shape(self.Z)
        n_q, n_q = np.shape(self.Q)

        k_g, n_g = np.shape(self.T)
        k_v, k_v = np.shape(self.H)

    def run(self):

        y = self.y
        a, s = self.a_prior, self.s_prior

        for t, d in enumerate(self.y.index):
            y_v = np.atleast_2d(y.loc[d])
            a_, s_ = self._update_equation(a, s, y_v, d)
            a, s = self._prediction_equation(a_, s_, d)

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

    def _update_equation(self, a, s, y, d):
        self._store_state(a, s, d)
        if np.isnan(y):
            return a, s
        # x_hat^F = x_hat + Sigma T' (T Sigma T' + H)^{-1}(y - T x_hat)
        # Sigma^F = Sigma - Sigma T' (T Sigma T' + H)^{-1} T Sigma

        Z, H = self.Z, self.H

        # x is the previous prediction of the state. We now observe a (noisy) y[t]. Combine information
        # Our prediction had noise, but so does our observation. What is the variance of our new signal?

        # Innovation or measurement pre-fit residual
        yk = (y - Z.dot(a))

        # Innovation of pre-fit covariance
        #sk = T * s * T.T + H
        sk = Z.dot(s).dot(Z.T) + H

        # Kalman gain is the matrix of population regression coefficients of the state x-x_hat
        # on the surprise y-Gx_hat
        #K = s * T.T * inv(sk)
        K = s.dot(Z.T).dot(inv(sk))

        # The new state is the prior state with the Kalman Gain multiplied by the implied state of the new observation
        # The combination between the two is based on the Kalman Gain. If H, which
        # is the covariance matrix of the state equation, is bigger the Kalman Gain is smaller, which means
        # We place less emphasis on the new observation. If the state variance-covariance is tiny, then we
        # trust the new measurement as probably-true.
        #x_hatF = x + K * yk
        #sigmaF = s - K * T * s

        a_hatF = a + K.dot(yk)
        sigmaF = s - K.dot(Z).dot(s)

        # post-fit residual
        # yk_k = (y - Z * a_hatF)

        return a_hatF, sigmaF

    def _prediction_equation(self, a_, s_, d):
        self._store_one_step_ahead_prediction(a_, s_, d)

        # Predicted (a priori) state estimate
        #x_ = self.Z * x_
        a_ = self.T.dot(a_)
        # Predicted (a priori) estimate covariance
        #s_ = self.Z * s_ * self.Z.transpose() + self.Q
        #s_ = self.T.dot(s_).dot(self.T.T) + self.R.dot(self.Q)
        s_ = self.T.dot(s_).dot(self.T.T) + self.R.dot(self.Q).dot(self.R.T)



        return a_, s_

    def _store_state(self, a, s, d):
        #self.output_data.loc[d , 'filtered_state'] = x
        self.output_data_list.append(a)

    def _store_one_step_ahead_prediction(self, a_, s_, d):
        #self.output_data.loc[d, 'one_step_ahead'] = x_
        self.output_prediction.append(a)

"""
# design
Z = np.array([ 1., 1., 0., 0.])

# transition
T = np.array([[ 1.,  0.,  0.,  0.],
       [ 0., -1., -1., -1.],
       [ 0.,  1., 0.,  0.],
       [ 0.,  0.,  1. ,  0.]])

# State cov
Q = np.array([[1.82,   0.00000000e+00], [  0.00000000e+00,   2.46095349e-11]])

R = np.array([[ 1.,  0.],
 [ 0.,  1.],
 [ 0.,  0.],
 [ 0.,  0.]])

# Obs cov
H = np.array([[  1.23]])

# state prior
a = np.array([[1.],
              [1.],
              [1.],
              [1.]])

# state variance
s = np.array([[1., 0, 0, 0],
              [0, 1., 0, 0],
              [0, 0, 1., 0],
              [0, 0, 0, 1.]])



filename = 'C:/Users/Simon/OneDrive/Documents/unobserved/IPGMFN.csv'
df = pd.read_csv(filename, header=0, index_col=0)
df = df.loc[df.index>'2002-12-01',:]
df.index = df.index.to_datetime()
#y = df.resample('Q').mean()
y=df

obj = Kalman(a_h=a, s=s, y=y, Z=Z, T=T, Q=Q, H=H, R=R)

obj.run()

print(1)


obj.output_data_list
x = []
for k in np.array(obj.output_data_list).tolist():
    x.append([j[0] for j in k])

print(1)




"""
"""
This type stub file was generated by pyright.
"""

from typing import Any, Callable, Protocol, TYPE_CHECKING

__all__ = ['fixed_quad', 'quadrature', 'romberg', 'romb', 'trapezoid', 'trapz', 'simps', 'simpson', 'cumulative_trapezoid', 'cumtrapz', 'newton_cotes', 'qmc_quad', 'AccuracyWarning']
def trapezoid(y, x=..., dx=..., axis=...): # -> Any:
    r"""
    Integrate along the given axis using the composite trapezoidal rule.

    If `x` is provided, the integration happens in sequence along its
    elements - they are not sorted.

    Integrate `y` (`x`) along each 1d slice on the given axis, compute
    :math:`\int y(x) dx`.
    When `x` is specified, this integrates along the parametric curve,
    computing :math:`\int_t y(t) dt =
    \int_t y(t) \left.\frac{dx}{dt}\right|_{x=x(t)} dt`.

    Parameters
    ----------
    y : array_like
        Input array to integrate.
    x : array_like, optional
        The sample points corresponding to the `y` values. If `x` is None,
        the sample points are assumed to be evenly spaced `dx` apart. The
        default is None.
    dx : scalar, optional
        The spacing between sample points when `x` is None. The default is 1.
    axis : int, optional
        The axis along which to integrate.

    Returns
    -------
    trapezoid : float or ndarray
        Definite integral of `y` = n-dimensional array as approximated along
        a single axis by the trapezoidal rule. If `y` is a 1-dimensional array,
        then the result is a float. If `n` is greater than 1, then the result
        is an `n`-1 dimensional array.

    See Also
    --------
    cumulative_trapezoid, simpson, romb

    Notes
    -----
    Image [2]_ illustrates trapezoidal rule -- y-axis locations of points
    will be taken from `y` array, by default x-axis distances between
    points will be 1.0, alternatively they can be provided with `x` array
    or with `dx` scalar.  Return value will be equal to combined area under
    the red lines.

    References
    ----------
    .. [1] Wikipedia page: https://en.wikipedia.org/wiki/Trapezoidal_rule

    .. [2] Illustration image:
           https://en.wikipedia.org/wiki/File:Composite_trapezoidal_rule_illustration.png

    Examples
    --------
    Use the trapezoidal rule on evenly spaced points:

    >>> import numpy as np
    >>> from scipy import integrate
    >>> integrate.trapezoid([1, 2, 3])
    4.0

    The spacing between sample points can be selected by either the
    ``x`` or ``dx`` arguments:

    >>> integrate.trapezoid([1, 2, 3], x=[4, 6, 8])
    8.0
    >>> integrate.trapezoid([1, 2, 3], dx=2)
    8.0

    Using a decreasing ``x`` corresponds to integrating in reverse:

    >>> integrate.trapezoid([1, 2, 3], x=[8, 6, 4])
    -8.0

    More generally ``x`` is used to integrate along a parametric curve. We can
    estimate the integral :math:`\int_0^1 x^2 = 1/3` using:

    >>> x = np.linspace(0, 1, num=50)
    >>> y = x**2
    >>> integrate.trapezoid(y, x)
    0.33340274885464394

    Or estimate the area of a circle, noting we repeat the sample which closes
    the curve:

    >>> theta = np.linspace(0, 2 * np.pi, num=1000, endpoint=True)
    >>> integrate.trapezoid(np.cos(theta), x=np.sin(theta))
    3.141571941375841

    ``trapezoid`` can be applied along a specified axis to do multiple
    computations in one call:

    >>> a = np.arange(6).reshape(2, 3)
    >>> a
    array([[0, 1, 2],
           [3, 4, 5]])
    >>> integrate.trapezoid(a, axis=0)
    array([1.5, 2.5, 3.5])
    >>> integrate.trapezoid(a, axis=1)
    array([2.,  8.])
    """
    ...

def trapz(y, x=..., dx=..., axis=...): # -> Any:
    """An alias of `trapezoid`.

    `trapz` is kept for backwards compatibility. For new code, prefer
    `trapezoid` instead.
    """
    ...

class AccuracyWarning(Warning):
    ...


if TYPE_CHECKING:
    class CacheAttributes(Protocol):
        cache: dict[int, tuple[Any, Any]]
        ...
    
    
else:
    ...
def cache_decorator(func: Callable) -> CacheAttributes:
    ...

def fixed_quad(func, a, b, args=..., n=...): # -> tuple[Unknown, None]:
    """
    Compute a definite integral using fixed-order Gaussian quadrature.

    Integrate `func` from `a` to `b` using Gaussian quadrature of
    order `n`.

    Parameters
    ----------
    func : callable
        A Python function or method to integrate (must accept vector inputs).
        If integrating a vector-valued function, the returned array must have
        shape ``(..., len(x))``.
    a : float
        Lower limit of integration.
    b : float
        Upper limit of integration.
    args : tuple, optional
        Extra arguments to pass to function, if any.
    n : int, optional
        Order of quadrature integration. Default is 5.

    Returns
    -------
    val : float
        Gaussian quadrature approximation to the integral
    none : None
        Statically returned value of None

    See Also
    --------
    quad : adaptive quadrature using QUADPACK
    dblquad : double integrals
    tplquad : triple integrals
    romberg : adaptive Romberg quadrature
    quadrature : adaptive Gaussian quadrature
    romb : integrators for sampled data
    simpson : integrators for sampled data
    cumulative_trapezoid : cumulative integration for sampled data
    ode : ODE integrator
    odeint : ODE integrator

    Examples
    --------
    >>> from scipy import integrate
    >>> import numpy as np
    >>> f = lambda x: x**8
    >>> integrate.fixed_quad(f, 0.0, 1.0, n=4)
    (0.1110884353741496, None)
    >>> integrate.fixed_quad(f, 0.0, 1.0, n=5)
    (0.11111111111111102, None)
    >>> print(1/9.0)  # analytical result
    0.1111111111111111

    >>> integrate.fixed_quad(np.cos, 0.0, np.pi/2, n=4)
    (0.9999999771971152, None)
    >>> integrate.fixed_quad(np.cos, 0.0, np.pi/2, n=5)
    (1.000000000039565, None)
    >>> np.sin(np.pi/2)-np.sin(0)  # analytical result
    1.0

    """
    ...

def vectorize1(func, args=..., vec_func=...): # -> (x: Unknown) -> Unknown:
    """Vectorize the call to a function.

    This is an internal utility function used by `romberg` and
    `quadrature` to create a vectorized version of a function.

    If `vec_func` is True, the function `func` is assumed to take vector
    arguments.

    Parameters
    ----------
    func : callable
        User defined function.
    args : tuple, optional
        Extra arguments for the function.
    vec_func : bool, optional
        True if the function func takes vector arguments.

    Returns
    -------
    vfunc : callable
        A function that will take a vector argument and return the
        result.

    """
    ...

def quadrature(func, a, b, args=..., tol=..., rtol=..., maxiter=..., vec_func=..., miniter=...): # -> tuple[Unknown | float, Unknown | float]:
    """
    Compute a definite integral using fixed-tolerance Gaussian quadrature.

    Integrate `func` from `a` to `b` using Gaussian quadrature
    with absolute tolerance `tol`.

    Parameters
    ----------
    func : function
        A Python function or method to integrate.
    a : float
        Lower limit of integration.
    b : float
        Upper limit of integration.
    args : tuple, optional
        Extra arguments to pass to function.
    tol, rtol : float, optional
        Iteration stops when error between last two iterates is less than
        `tol` OR the relative change is less than `rtol`.
    maxiter : int, optional
        Maximum order of Gaussian quadrature.
    vec_func : bool, optional
        True or False if func handles arrays as arguments (is
        a "vector" function). Default is True.
    miniter : int, optional
        Minimum order of Gaussian quadrature.

    Returns
    -------
    val : float
        Gaussian quadrature approximation (within tolerance) to integral.
    err : float
        Difference between last two estimates of the integral.

    See Also
    --------
    romberg : adaptive Romberg quadrature
    fixed_quad : fixed-order Gaussian quadrature
    quad : adaptive quadrature using QUADPACK
    dblquad : double integrals
    tplquad : triple integrals
    romb : integrator for sampled data
    simpson : integrator for sampled data
    cumulative_trapezoid : cumulative integration for sampled data
    ode : ODE integrator
    odeint : ODE integrator

    Examples
    --------
    >>> from scipy import integrate
    >>> import numpy as np
    >>> f = lambda x: x**8
    >>> integrate.quadrature(f, 0.0, 1.0)
    (0.11111111111111106, 4.163336342344337e-17)
    >>> print(1/9.0)  # analytical result
    0.1111111111111111

    >>> integrate.quadrature(np.cos, 0.0, np.pi/2)
    (0.9999999999999536, 3.9611425250996035e-11)
    >>> np.sin(np.pi/2)-np.sin(0)  # analytical result
    1.0

    """
    ...

def tupleset(t, i, value): # -> tuple[Unknown, ...]:
    ...

def cumtrapz(y, x=..., dx=..., axis=..., initial=...): # -> NDArray[floating[Any]]:
    """An alias of `cumulative_trapezoid`.

    `cumtrapz` is kept for backwards compatibility. For new code, prefer
    `cumulative_trapezoid` instead.
    """
    ...

def cumulative_trapezoid(y, x=..., dx=..., axis=..., initial=...): # -> NDArray[floating[Any]]:
    """
    Cumulatively integrate y(x) using the composite trapezoidal rule.

    Parameters
    ----------
    y : array_like
        Values to integrate.
    x : array_like, optional
        The coordinate to integrate along. If None (default), use spacing `dx`
        between consecutive elements in `y`.
    dx : float, optional
        Spacing between elements of `y`. Only used if `x` is None.
    axis : int, optional
        Specifies the axis to cumulate. Default is -1 (last axis).
    initial : scalar, optional
        If given, insert this value at the beginning of the returned result.
        Typically this value should be 0. Default is None, which means no
        value at ``x[0]`` is returned and `res` has one element less than `y`
        along the axis of integration.

    Returns
    -------
    res : ndarray
        The result of cumulative integration of `y` along `axis`.
        If `initial` is None, the shape is such that the axis of integration
        has one less value than `y`. If `initial` is given, the shape is equal
        to that of `y`.

    See Also
    --------
    numpy.cumsum, numpy.cumprod
    quad : adaptive quadrature using QUADPACK
    romberg : adaptive Romberg quadrature
    quadrature : adaptive Gaussian quadrature
    fixed_quad : fixed-order Gaussian quadrature
    dblquad : double integrals
    tplquad : triple integrals
    romb : integrators for sampled data
    ode : ODE integrators
    odeint : ODE integrators

    Examples
    --------
    >>> from scipy import integrate
    >>> import numpy as np
    >>> import matplotlib.pyplot as plt

    >>> x = np.linspace(-2, 2, num=20)
    >>> y = x
    >>> y_int = integrate.cumulative_trapezoid(y, x, initial=0)
    >>> plt.plot(x, y_int, 'ro', x, y[0] + 0.5 * x**2, 'b-')
    >>> plt.show()

    """
    ...

def simps(y, x=..., dx=..., axis=..., even=...): # -> NDArray[floating[Any]] | float:
    """An alias of `simpson`.

    `simps` is kept for backwards compatibility. For new code, prefer
    `simpson` instead.
    """
    ...

def simpson(y, x=..., dx=..., axis=..., even=...): # -> NDArray[floating[Any]] | float:
    """
    Integrate y(x) using samples along the given axis and the composite
    Simpson's rule. If x is None, spacing of dx is assumed.

    If there are an even number of samples, N, then there are an odd
    number of intervals (N-1), but Simpson's rule requires an even number
    of intervals. The parameter 'even' controls how this is handled.

    Parameters
    ----------
    y : array_like
        Array to be integrated.
    x : array_like, optional
        If given, the points at which `y` is sampled.
    dx : float, optional
        Spacing of integration points along axis of `x`. Only used when
        `x` is None. Default is 1.
    axis : int, optional
        Axis along which to integrate. Default is the last axis.
    even : {None, 'simpson', 'avg', 'first', 'last'}, optional
        'avg' : Average two results:
            1) use the first N-2 intervals with
               a trapezoidal rule on the last interval and
            2) use the last
               N-2 intervals with a trapezoidal rule on the first interval.

        'first' : Use Simpson's rule for the first N-2 intervals with
                a trapezoidal rule on the last interval.

        'last' : Use Simpson's rule for the last N-2 intervals with a
               trapezoidal rule on the first interval.

        None : equivalent to 'simpson' (default)

        'simpson' : Use Simpson's rule for the first N-2 intervals with the
                  addition of a 3-point parabolic segment for the last
                  interval using equations outlined by Cartwright [1]_.
                  If the axis to be integrated over only has two points then
                  the integration falls back to a trapezoidal integration.

                  .. versionadded:: 1.11.0

        .. versionchanged:: 1.11.0
            The newly added 'simpson' option is now the default as it is more
            accurate in most situations.

        .. deprecated:: 1.11.0
            Parameter `even` is deprecated and will be removed in SciPy
            1.13.0. After this time the behaviour for an even number of
            points will follow that of `even='simpson'`.

    Returns
    -------
    float
        The estimated integral computed with the composite Simpson's rule.

    See Also
    --------
    quad : adaptive quadrature using QUADPACK
    romberg : adaptive Romberg quadrature
    quadrature : adaptive Gaussian quadrature
    fixed_quad : fixed-order Gaussian quadrature
    dblquad : double integrals
    tplquad : triple integrals
    romb : integrators for sampled data
    cumulative_trapezoid : cumulative integration for sampled data
    ode : ODE integrators
    odeint : ODE integrators

    Notes
    -----
    For an odd number of samples that are equally spaced the result is
    exact if the function is a polynomial of order 3 or less. If
    the samples are not equally spaced, then the result is exact only
    if the function is a polynomial of order 2 or less.

    References
    ----------
    .. [1] Cartwright, Kenneth V. Simpson's Rule Cumulative Integration with
           MS Excel and Irregularly-spaced Data. Journal of Mathematical
           Sciences and Mathematics Education. 12 (2): 1-9

    Examples
    --------
    >>> from scipy import integrate
    >>> import numpy as np
    >>> x = np.arange(0, 10)
    >>> y = np.arange(0, 10)

    >>> integrate.simpson(y, x)
    40.5

    >>> y = np.power(x, 3)
    >>> integrate.simpson(y, x)
    1640.5
    >>> integrate.quad(lambda x: x**3, 0, 9)[0]
    1640.25

    >>> integrate.simpson(y, x, even='first')
    1644.5

    """
    ...

def romb(y, dx=..., axis=..., show=...):
    """
    Romberg integration using samples of a function.

    Parameters
    ----------
    y : array_like
        A vector of ``2**k + 1`` equally-spaced samples of a function.
    dx : float, optional
        The sample spacing. Default is 1.
    axis : int, optional
        The axis along which to integrate. Default is -1 (last axis).
    show : bool, optional
        When `y` is a single 1-D array, then if this argument is True
        print the table showing Richardson extrapolation from the
        samples. Default is False.

    Returns
    -------
    romb : ndarray
        The integrated result for `axis`.

    See Also
    --------
    quad : adaptive quadrature using QUADPACK
    romberg : adaptive Romberg quadrature
    quadrature : adaptive Gaussian quadrature
    fixed_quad : fixed-order Gaussian quadrature
    dblquad : double integrals
    tplquad : triple integrals
    simpson : integrators for sampled data
    cumulative_trapezoid : cumulative integration for sampled data
    ode : ODE integrators
    odeint : ODE integrators

    Examples
    --------
    >>> from scipy import integrate
    >>> import numpy as np
    >>> x = np.arange(10, 14.25, 0.25)
    >>> y = np.arange(3, 12)

    >>> integrate.romb(y)
    56.0

    >>> y = np.sin(np.power(x, 2.5))
    >>> integrate.romb(y)
    -0.742561336672229

    >>> integrate.romb(y, show=True)
    Richardson Extrapolation Table for Romberg Integration
    ======================================================
    -0.81576
     4.63862  6.45674
    -1.10581 -3.02062 -3.65245
    -2.57379 -3.06311 -3.06595 -3.05664
    -1.34093 -0.92997 -0.78776 -0.75160 -0.74256
    ======================================================
    -0.742561336672229  # may vary

    """
    ...

def romberg(function, a, b, args=..., tol=..., rtol=..., show=..., divmax=..., vec_func=...):
    """
    Romberg integration of a callable function or method.

    Returns the integral of `function` (a function of one variable)
    over the interval (`a`, `b`).

    If `show` is 1, the triangular array of the intermediate results
    will be printed. If `vec_func` is True (default is False), then
    `function` is assumed to support vector arguments.

    Parameters
    ----------
    function : callable
        Function to be integrated.
    a : float
        Lower limit of integration.
    b : float
        Upper limit of integration.

    Returns
    -------
    results : float
        Result of the integration.

    Other Parameters
    ----------------
    args : tuple, optional
        Extra arguments to pass to function. Each element of `args` will
        be passed as a single argument to `func`. Default is to pass no
        extra arguments.
    tol, rtol : float, optional
        The desired absolute and relative tolerances. Defaults are 1.48e-8.
    show : bool, optional
        Whether to print the results. Default is False.
    divmax : int, optional
        Maximum order of extrapolation. Default is 10.
    vec_func : bool, optional
        Whether `func` handles arrays as arguments (i.e., whether it is a
        "vector" function). Default is False.

    See Also
    --------
    fixed_quad : Fixed-order Gaussian quadrature.
    quad : Adaptive quadrature using QUADPACK.
    dblquad : Double integrals.
    tplquad : Triple integrals.
    romb : Integrators for sampled data.
    simpson : Integrators for sampled data.
    cumulative_trapezoid : Cumulative integration for sampled data.
    ode : ODE integrator.
    odeint : ODE integrator.

    References
    ----------
    .. [1] 'Romberg's method' https://en.wikipedia.org/wiki/Romberg%27s_method

    Examples
    --------
    Integrate a gaussian from 0 to 1 and compare to the error function.

    >>> from scipy import integrate
    >>> from scipy.special import erf
    >>> import numpy as np
    >>> gaussian = lambda x: 1/np.sqrt(np.pi) * np.exp(-x**2)
    >>> result = integrate.romberg(gaussian, 0, 1, show=True)
    Romberg integration of <function vfunc at ...> from [0, 1]

    ::

       Steps  StepSize  Results
           1  1.000000  0.385872
           2  0.500000  0.412631  0.421551
           4  0.250000  0.419184  0.421368  0.421356
           8  0.125000  0.420810  0.421352  0.421350  0.421350
          16  0.062500  0.421215  0.421350  0.421350  0.421350  0.421350
          32  0.031250  0.421317  0.421350  0.421350  0.421350  0.421350  0.421350

    The final result is 0.421350396475 after 33 function evaluations.

    >>> print("%g %g" % (2*result, erf(1)))
    0.842701 0.842701

    """
    ...

_builtincoeffs = ...
def newton_cotes(rn, equal=...): # -> tuple[Unknown, Unknown] | tuple[Any | Unknown, Any | Unknown]:
    r"""
    Return weights and error coefficient for Newton-Cotes integration.

    Suppose we have (N+1) samples of f at the positions
    x_0, x_1, ..., x_N. Then an N-point Newton-Cotes formula for the
    integral between x_0 and x_N is:

    :math:`\int_{x_0}^{x_N} f(x)dx = \Delta x \sum_{i=0}^{N} a_i f(x_i)
    + B_N (\Delta x)^{N+2} f^{N+1} (\xi)`

    where :math:`\xi \in [x_0,x_N]`
    and :math:`\Delta x = \frac{x_N-x_0}{N}` is the average samples spacing.

    If the samples are equally-spaced and N is even, then the error
    term is :math:`B_N (\Delta x)^{N+3} f^{N+2}(\xi)`.

    Parameters
    ----------
    rn : int
        The integer order for equally-spaced data or the relative positions of
        the samples with the first sample at 0 and the last at N, where N+1 is
        the length of `rn`. N is the order of the Newton-Cotes integration.
    equal : int, optional
        Set to 1 to enforce equally spaced data.

    Returns
    -------
    an : ndarray
        1-D array of weights to apply to the function at the provided sample
        positions.
    B : float
        Error coefficient.

    Notes
    -----
    Normally, the Newton-Cotes rules are used on smaller integration
    regions and a composite rule is used to return the total integral.

    Examples
    --------
    Compute the integral of sin(x) in [0, :math:`\pi`]:

    >>> from scipy.integrate import newton_cotes
    >>> import numpy as np
    >>> def f(x):
    ...     return np.sin(x)
    >>> a = 0
    >>> b = np.pi
    >>> exact = 2
    >>> for N in [2, 4, 6, 8, 10]:
    ...     x = np.linspace(a, b, N + 1)
    ...     an, B = newton_cotes(N, 1)
    ...     dx = (b - a) / N
    ...     quad = dx * np.sum(an * f(x))
    ...     error = abs(quad - exact)
    ...     print('{:2d}  {:10.9f}  {:.5e}'.format(N, quad, error))
    ...
     2   2.094395102   9.43951e-02
     4   1.998570732   1.42927e-03
     6   2.000017814   1.78136e-05
     8   1.999999835   1.64725e-07
    10   2.000000001   1.14677e-09

    """
    ...

QMCQuadResult = ...
def qmc_quad(func, a, b, *, n_estimates=..., n_points=..., qrng=..., log=...): # -> QMCQuadResult:
    """
    Compute an integral in N-dimensions using Quasi-Monte Carlo quadrature.

    Parameters
    ----------
    func : callable
        The integrand. Must accept a single argument ``x``, an array which
        specifies the point(s) at which to evaluate the scalar-valued
        integrand, and return the value(s) of the integrand.
        For efficiency, the function should be vectorized to accept an array of
        shape ``(d, n_points)``, where ``d`` is the number of variables (i.e.
        the dimensionality of the function domain) and `n_points` is the number
        of quadrature points, and return an array of shape ``(n_points,)``,
        the integrand at each quadrature point.
    a, b : array-like
        One-dimensional arrays specifying the lower and upper integration
        limits, respectively, of each of the ``d`` variables.
    n_estimates, n_points : int, optional
        `n_estimates` (default: 8) statistically independent QMC samples, each
        of `n_points` (default: 1024) points, will be generated by `qrng`.
        The total number of points at which the integrand `func` will be
        evaluated is ``n_points * n_estimates``. See Notes for details.
    qrng : `~scipy.stats.qmc.QMCEngine`, optional
        An instance of the QMCEngine from which to sample QMC points.
        The QMCEngine must be initialized to a number of dimensions ``d``
        corresponding with the number of variables ``x1, ..., xd`` passed to
        `func`.
        The provided QMCEngine is used to produce the first integral estimate.
        If `n_estimates` is greater than one, additional QMCEngines are
        spawned from the first (with scrambling enabled, if it is an option.)
        If a QMCEngine is not provided, the default `scipy.stats.qmc.Halton`
        will be initialized with the number of dimensions determine from
        the length of `a`.
    log : boolean, default: False
        When set to True, `func` returns the log of the integrand, and
        the result object contains the log of the integral.

    Returns
    -------
    result : object
        A result object with attributes:

        integral : float
            The estimate of the integral.
        standard_error :
            The error estimate. See Notes for interpretation.

    Notes
    -----
    Values of the integrand at each of the `n_points` points of a QMC sample
    are used to produce an estimate of the integral. This estimate is drawn
    from a population of possible estimates of the integral, the value of
    which we obtain depends on the particular points at which the integral
    was evaluated. We perform this process `n_estimates` times, each time
    evaluating the integrand at different scrambled QMC points, effectively
    drawing i.i.d. random samples from the population of integral estimates.
    The sample mean :math:`m` of these integral estimates is an
    unbiased estimator of the true value of the integral, and the standard
    error of the mean :math:`s` of these estimates may be used to generate
    confidence intervals using the t distribution with ``n_estimates - 1``
    degrees of freedom. Perhaps counter-intuitively, increasing `n_points`
    while keeping the total number of function evaluation points
    ``n_points * n_estimates`` fixed tends to reduce the actual error, whereas
    increasing `n_estimates` tends to decrease the error estimate.

    Examples
    --------
    QMC quadrature is particularly useful for computing integrals in higher
    dimensions. An example integrand is the probability density function
    of a multivariate normal distribution.

    >>> import numpy as np
    >>> from scipy import stats
    >>> dim = 8
    >>> mean = np.zeros(dim)
    >>> cov = np.eye(dim)
    >>> def func(x):
    ...     # `multivariate_normal` expects the _last_ axis to correspond with
    ...     # the dimensionality of the space, so `x` must be transposed
    ...     return stats.multivariate_normal.pdf(x.T, mean, cov)

    To compute the integral over the unit hypercube:

    >>> from scipy.integrate import qmc_quad
    >>> a = np.zeros(dim)
    >>> b = np.ones(dim)
    >>> rng = np.random.default_rng()
    >>> qrng = stats.qmc.Halton(d=dim, seed=rng)
    >>> n_estimates = 8
    >>> res = qmc_quad(func, a, b, n_estimates=n_estimates, qrng=qrng)
    >>> res.integral, res.standard_error
    (0.00018429555666024108, 1.0389431116001344e-07)

    A two-sided, 99% confidence interval for the integral may be estimated
    as:

    >>> t = stats.t(df=n_estimates-1, loc=res.integral,
    ...             scale=res.standard_error)
    >>> t.interval(0.99)
    (0.0001839319802536469, 0.00018465913306683527)

    Indeed, the value reported by `scipy.stats.multivariate_normal` is
    within this range.

    >>> stats.multivariate_normal.cdf(b, mean, cov, lower_limit=a)
    0.00018430867675187443

    """
    ...


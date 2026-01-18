pyMULTALL package
=================

Subpackages
-----------

.. toctree::
   :maxdepth: 4

   pyMULTALL.meangen
   pyMULTALL.multall
   pyMULTALL.plotutils
   pyMULTALL.stagen

Submodules
----------

pyMULTALL.auxiliaries module
----------------------------

.. automodule:: pyMULTALL.auxiliaries
   :members:
   :show-inheritance:
   :undoc-members:

pyMULTALL.defaults module
-------------------------

.. automodule:: pyMULTALL.defaults
   :members:
   :show-inheritance:
   :undoc-members:

pyMULTALL.thermo module
-----------------------

For an **ideal gas** (:math:`p/{\rho} = RT` and :math:`c_p = c_p(T)`) it can be 
shown that :math:`dh = c_p dT` always, no matter the process. Therefore the 
enthalpy change for an ideal gas is

.. math::

        h = h_{ref} + \int_{T_{ref}}^T c_p({\tau}) d{\tau}

For a **perfect gas** (:math:`p/{\rho} = RT` and :math:`c_p = \text{const.}`), 
this reduces to the familiar

.. math::

        h = h_{ref} + c_p(T - T_{ref})

NASA polynomials are a specific and widely-used case of ideal-gas :math:`c_p(T)`,
where the constant-pressure specific heat is modelled as [McBride2002]_

.. math::

		\frac{c_p}{T} = \frac{a_1}{T^2} + \frac{a_2}{T} + a_3 + a_4 T + a_5 T^2 + a_6 T^3 + a_7 T^4

The enthalpy is then obtained by analytical integration of :math:`c_p(T)` as

.. math::

		\frac{h^0}{RT} = - \frac{a_1}{T^2} + a_2\frac{\ln T}{T} + a_3 + a_4 \frac{T}{2} + a_5 \frac{T^2}{3} + a_6 \frac{T^3}{4} + a_7 \frac{T^4}{5} + \frac{a_8}{T}

The entropy for an **ideal gas** is obtained by integrating 

.. math::

		ds = c_p \frac{dT}{T} - \frac{v}{T} dp = c_p \frac{dT}{T} - R \frac{dp}{p}

(obtained from :math:`dh = Tds + vdp = c_p dT`), leading to

.. math::

		s(T,p) = s_{ref} + \int_{T_{ref}}^T c_p(\tau) \frac{d\tau}{\tau} - R \ln\bigg(\frac{p}{p_{ref}}\bigg)

Therefore the :math:`s` *always* depends on both :math:`p` and :math:`T`. However,
:math:`s` is split into two contributions:

- a temperature-dependent one, which requires numerical integration of

.. math::

		\int_{T_{ref}}^T c_p(\tau) \frac{d\tau}{\tau}

- a pressure-dependent one, which is already written in closed form as

.. math::

		- R \ln\bigg(\frac{p}{p_{ref}}\bigg)

Using NASA polynomials, the temperature-dependent term can be analytically
integrated (and is labelled :math:`s^0` in [McBride2002]_)

.. math::

		\frac{s^0}{R} = - \frac{a_1}{2 T^2} - \frac{a_2}{T} + a_3 \ln{T} + a_4 T + a_5 \frac{T^2}{2} + a_6 \frac{T^3}{3} + a_7 \frac{T^4}{4} + a_9

Of course for a **perfect gas** the entropy is just

.. math::
	
		s(T,p) = s_{ref} + c_p \ln\bigg(\frac{T}{T_{ref}}\bigg) - R \ln\bigg(\frac{p}{p_{ref}}\bigg)

References
----------
.. [McBride2002] McBride, B. J. et al.: NASA Glenn Coefficients for Calculating
	Thermodynamic Properties of Individual Species, NASA Technical Publication 
	2002-211556, URL: `<https://ntrs.nasa.gov/citations/20020085330>`_

.. automodule:: pyMULTALL.thermo
   :members:
   :show-inheritance:
   :undoc-members:

Module contents
---------------

.. automodule:: pyMULTALL
   :members:
   :show-inheritance:
   :undoc-members:

#include <pybind11/pybind11.h>
#include <pybind11/operators.h>

#include "tcurve.h"

namespace py = pybind11;


PYBIND11_MODULE(tcurve, m)
{
    m.doc() = "TCurve trajectory generation library";


    // -------------------------------
    // Enums
    // -------------------------------

    py::enum_<TCurveError>(m, "TCurveError")
        .value("OK", TCurveError::OK)
        .value("NotOk", TCurveError::NotOk)
        .value("InvalidSetting", TCurveError::InvalidSetting)
        .value("MustBeNonZeroFinite", TCurveError::MustBeNonZeroFinite)
        .value("TimeOutOfRange", TCurveError::TimeOutOfRange)
        .value("NotImplemented", TCurveError::NotImplemented)
        .value("NotInitialized", TCurveError::NotInitialized);


    py::enum_<TCurveType>(m, "TCurveType")
        .value("TCurve", TCurveType::TCurve)
        .value("SCurve", TCurveType::SCurve)
        .value("NotInitialized", TCurveType::NotInitialized);



    // -------------------------------
    // TCurve class
    // -------------------------------

    py::class_<TCurve>(m, "TCurve")

        .def(py::init<>())

        .def(
            "set_acceleration",
            &TCurve::setAcceleration,
            py::arg("acceleration")
        )

        .def(
            "set_max_velocity",
            &TCurve::setMaxVelocity,
            py::arg("velocity")
        )

        .def(
            "set_delta_phi",
            &TCurve::setDeltaPhi,
            py::arg("delta_phi")
        )


        .def(
            "get_point",
            [](TCurve& self, float t)
            {
                float value;
                TCurveError err = self.getPoint(t, &value);

                return py::make_tuple(err, value);
            },
            py::arg("time")
        )


        .def(
            "recalculate",
            &TCurve::recalculateInternalVariables
        )


        .def(
            "get_curve_type",
            &TCurve::getCurveType
        )

        .def(
            "get_acceleration",
            &TCurve::getAcceleration
        )

        .def(
            "get_max_velocity",
            &TCurve::getMaxVelocity
        )

        .def(
            "get_delta_phi",
            &TCurve::getDeltaPhi
        )

        .def(
            "get_t1",
            &TCurve::getT1
        )

        .def(
            "get_t2",
            &TCurve::getT2
        )

        .def(
            "get_tmax",
            &TCurve::getTMax
        )

        .def(
            "get_wmax",
            &TCurve::getWMax
        );
}
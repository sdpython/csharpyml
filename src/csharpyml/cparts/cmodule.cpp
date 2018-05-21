#include "version.hpp"
#include <stdio.h>
#include <vector>
#include <stdexcept>
#include "Python.h"

struct module_state {
    PyObject *error;
};

#define GETSTATE(m) ((struct module_state*)PyModule_GetState(m))


///////////////////////////////////////////////
//////////// python function //////////////////
///////////////////////////////////////////////

static PyObject* version_c(PyObject *self, PyObject *unused)
{
    PyObject * message = Py_BuildValue("s", VersionC());
    if (message == NULL)
        throw new std::runtime_error("Unable to retrieve the version.");
    Py_INCREF(message);
    return message;
}

////////////////////////////////////////////////////
//////////// module definition /////////////////////
////////////////////////////////////////////////////

const char * module_name = "cmodule" ;

static int cmodule_module_traverse(PyObject *m, visitproc visit, void *arg) {
    Py_VISIT(GETSTATE(m)->error);
    return 0;
}

static int cmodule_module_clear(PyObject *m) {
    Py_CLEAR(GETSTATE(m)->error);
    return 0;
}

static PyMethodDef fonctions [] = {
  {"version_c",  version_c, METH_VARARGS, "Retrieves the version for the C parts."},
  {NULL, NULL}
} ;

static struct PyModuleDef moduledef = {
        PyModuleDef_HEAD_INIT,
        module_name,
        "C++ Helpers.",
        sizeof(struct module_state),
        fonctions,
        NULL,
        cmodule_module_traverse,
        cmodule_module_clear,
        NULL
};

#ifdef __cplusplus
extern "C" { 
#endif


PyObject * 
PyInit_cmodule(void)
{
    PyObject* m ;
    m = PyModule_Create(&moduledef);
    if (m == NULL)
        return NULL;
    
    struct module_state *st = GETSTATE(m);
    if (st == NULL)
        throw new std::runtime_error("GETSTATE returns null.");

    st->error = PyErr_NewException("cmodule.Error", NULL, NULL);
    if (st->error == NULL) {
        Py_DECREF(m);
        return NULL;
    }
    
    return m ;
}


#ifdef __cplusplus
}
#endif

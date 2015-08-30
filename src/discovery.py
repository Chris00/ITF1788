#
#                              ITF1788
#
#   Interval Test Framework for IEEE 1788 Standard for Interval Arithmetic
#
#
#   Copyright 2014
#
#   Marco Nehmeier (nehmeier@informatik.uni-wuerzburg.de)
#   Maximilian Kiesner (maximilian.kiesner@stud-mail.uni-wuerzburg.de)
#
#   Department of Computer Science
#   University of Wuerzburg, Germany
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import os
import yaml

# path to plugin folder
PLUGIN_PATH = 'plugins'


def getSpecification(lang, testLib, arithLib):
    """
    Return a complete specification as a tuple of dictionaries.

    Arguments:
    lang -- the name of the language
    testLib -- the name of the test library
    arithLib -- the name of the interval library
    """
    langDict = getLanguageSpecification(lang)
    testLibDict = getTestLibSpecification(lang, testLib)
    arithLibDict = getArithLibSpecification(lang, arithLib)
    return (langDict, testLibDict, arithLibDict)


def getCbPath(lang):
    """
    Return the path to the callbacks.py module in python notation.

    For the language 'cpp' the function return '..plugins.cpp.callbacks.py'.
    Return None if no such module exists.

    Arguments:
    lang -- the name of the language
    """
    path = '/'.join([os.path.dirname(__file__), PLUGIN_PATH, lang, 'callbacks.py'])
    if not exists(path):
        # no error, callbacks are simply not used
        return None
    # The callback will be imported by the testAST module,
    # so the path must be prefixed with “..”.
    modulePath = '.'.join([".", PLUGIN_PATH, lang, 'callbacks'])
    return modulePath


def getLanguageSpecification(lang):
    """
    Return a dictionary which contains the specification of a language.

    Specifically, return the key-value pairs defined in the 'lang.yaml' file as
    a dictionary, i.e. for the language cpp return the contents of
    'plugins/cpp/lang.yaml'.
    Raise an IOError if the 'lang.yaml' file does not exist.

    Arguments:
    lang -- the name of the language
    """
    dirPath = '/'.join([os.path.dirname(__file__), PLUGIN_PATH, lang])
    if not exists(dirPath):
        print('ERROR:', dirPath, 'dir not found.')
        raise IOError()
    filePath = '/'.join([dirPath, 'lang.yaml'])
    if not exists(filePath):
        print('ERROR: lang.yaml file not found for language', lang)
        raise IOError()
    return yaml.load(open(filePath).read().strip())


def getTestLibSpecification(lang, testLib):
    """
    Return a dictionary which contains the specification of the test library.

    Specifically, return the key-value pairs defined in the 'test.yaml' file as
    a dictionary, i.e. for the language cpp and the test library BOOST return
    the contents of 'plugins/cpp/test/BOOST/test.yaml'.
    Raise an IOError if the 'test.yaml' file does not exist.

    Arguments:
    lang -- the name of the language
    testLib -- the name of the test library
    """
    dirPath = '/'.join([os.path.dirname(__file__), PLUGIN_PATH, lang, 'test', testLib])
    if not exists(dirPath):
        print('ERROR:', dirPath, 'dir not found.')
        raise IOError()
    filePath = '/'.join([dirPath, 'test.yaml'])
    if not exists(filePath):
        print('ERROR: test.yaml file not found for language ', lang,
                      ', testing framework ', testLib)
        raise IOError()
    return yaml.load(open(filePath).read().strip())


def getArithLibSpecification(lang, arithLib):
    """
    Return a dictionary with the specification of the interval library.

    Specifically, return the key-value pairs defined in the 'arith.yaml' file
    as a dictionary, i.e. for the language cüü and the interval library lib1
    return the contents of 'plugins/cpp/arith/lib1/arith.yaml'.
    Raise an IOError if the file is not found.

    Arguments:
    lang -- the name of the language
    arithLib -- the name of the interval library
    """
    dirPath = '/'.join([os.path.dirname(__file__), PLUGIN_PATH, lang, 'arith', arithLib])
    if not exists(dirPath):
        print('ERROR:', dirPath, 'dir not found.')
        raise IOError()
    filePath = '/'.join([dirPath, 'arith.yaml'])
    if not exists(filePath):
        print('ERROR: test.yaml file not found for language', lang,
                      ', IEEE 1788 library ', arithLib)
        raise IOError()
    return yaml.load(open(filePath).read().strip())


def getSpecList():
    """
    Return a list of all valid specifications.

    Specifically, return a list of tuples (language, testLib, intervalLib)
    where the elements of the tuples represent their names (rather than their
    content).
    """
    specs = []

    # assemble all languages
    langs = getSubLibs(os.path.dirname(__file__) + "/" + PLUGIN_PATH)

    for lang in langs:
        arithPath = os.path.dirname(__file__) + "/" + PLUGIN_PATH + "/" + lang + "/arith/"
        if not exists(arithPath):
            print('ERROR: Can not get speclist: Path', arithPath, 'does not exist')
            raise IOError()
        ariths = getSubLibs(arithPath)

        testPath = os.path.dirname(__file__) + "/" + PLUGIN_PATH + "/" + lang + "/test/"
        if not exists(testPath):
            print('ERROR: Can not get speclist: Path', testPath, 'does not exist')
            raise IOError()
        tests = getSubLibs(testPath)

        for test in tests:
            for arith in ariths:
                specs += [(lang, test, arith)]
    return specs


def getSpecListByLanguageAndTestLibrary(lang, testLib):
    """
    Return a list of specifications by the language and test library names.

    Specifically, return a list of tuples (language, testLib, intervalLib)
    where the language and the test library are defined by the parameters and
    the interval library is variable.

    Arguments:
    lang -- the name of the language
    testLib -- the name of the test library
    """
    specs = []

    arithPath = os.path.dirname(__file__) + "/" + PLUGIN_PATH + "/" + lang + "/arith/"
    if not exists(arithPath):
        raise IOError('Can not get speclist: Path', arithPath, 'does not exist')
    
    ariths = getSubLibs(arithPath)

    for arith in ariths:
        specs += [(lang, testLib, arith)]

    return specs


def getSpecListByLanguageAndArithmeticLibrary(lang, arithLib):
    """
    Return a list of specifications by language and interval library names.

    Specifically, return a list of tuples (language, testLib, intervalLib)
    where the language and the interval library are defined by the parameters
    and the test library is variable.

    Arguments:
    lang -- the name of the language
    arithLib -- the name of the interval library
    """
    specs = []

    testPath = os.path.dirname(__file__) + "/" + PLUGIN_PATH + "/" + lang + "/test/"
    if not exists(testPath):
        raise IOError('Can not get speclist: Path', testPath, 'does not exist')
        
    tests = getSubLibs(testPath)

    for test in tests:
        specs += [(lang, test, arithLib)]

    return specs


def getSpecListByLanguage(lang):
    """
    Return a list of specifications by the language.

    Specifically, return a list of tuples (language, testLib, intervalLib)
    where the language is defined by the parameter and the test library
    and the interval library are variable.

    Arguments:
    lang -- the name of the language
    """
    specs = []

    arithPath = os.path.dirname(__file__) + "/" + PLUGIN_PATH + "/" + lang + "/arith/"
    if not exists(arithPath):
        raise IOError('Can not get speclist: Path', arithPath, 'does not exist')
        
    ariths = getSubLibs(arithPath)

    testPath = os.path.dirname(__file__) + "/" + PLUGIN_PATH + "/" + lang + "/test/"
    if not exists(testPath):
        raise IOError('Can not get speclist: Path', testPath, 'does not exist')
    tests = getSubLibs(testPath)

    for test in tests:
        for arith in ariths:
            specs += [(lang, test, arith)]
    return specs


def getSubDirs(path):
    """
    Return a list of all immediate subdirectories of a path.

    Raise an IOError if path does not represent a directory.

    Arguments:
    path -- path to the directory
    """
    if not os.path.isdir(path):
        raise IOError(path + ' is not a directory')
    return [name for name in os.listdir(path)
            if os.path.isdir(os.path.join(path, name))]


def getSubLibs(path):
    """
    Return a list of immediate subdirectories without the __pycache__ folder.

    Raise an IOError if path does not exist.

    Arguments:
    path -- path to the directory
    """
    return list(filter(lambda x: x != '__pycache__', getSubDirs(path)))


def exists(path):
    """
    Checks if the absolute value of path is a valid directory.

    Arguments:
    path -- path to the directory
    """
    return os.path.exists(os.path.abspath(path))

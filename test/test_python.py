import unittest

class PythonLanguageTest(unittest.TestCase):
    def testListEquals(self):
        liste = [1,2,3]
        list2 = [1,2,3]
        list3 = [1,2,4]

        self.assertEqual(liste, list2)
        self.assertNotEqual(liste, list3)
        self.assertTrue(liste == list2)
        self.assertFalse(liste == list3)

    def testListIndexing(self):
        liste = [1,2,3]
        self.assertEqual(liste[0],1)
        #self.assertRaises(IndexError, liste[len(liste)])

    def testTuples(self):
        meinTupel = 5,
        self.assertTrue(isinstance(meinTupel,tuple))

    def testTupelCompare(self):
        myList = [1,2,5]
        self.assertTrue( myList ==[1,2,5])

        myListB = [1,2,6]
        self.assertFalse(myListB == myList)
        myListB[2] = 5
        self.assertTrue(myListB == myList)

    def testTupleOfEmptyness(self):
        leerTupel = ()
        self.assertTrue(isinstance(leerTupel, tuple))
        leerTupel = ((),)
        self.assertTrue(isinstance(leerTupel[0], tuple))

        leerTupel = (()) # same as "leertupel = ()"
        self.assertRaises(IndexError, lambda: leerTupel[0])

    def testCounterVariablesOverwrite(self):
        x = 10
        for x in range(20,30):
            y = x
        self.assertEqual(x,29)
        self.assertEqual(y,29)

        k = 0
        for z in range(3):
            for z in range(10,20):
                k = k + 1
        self.assertEqual(k,30)

    def testRangeObject(self):
        b = range(1,3)
        self.assertTrue(isinstance(b,range))

    def testRangeStartEnd(self):
        got5 = False
        got10 = False
        for i in range(5,10):
            if (i==5):
                got5 = True
            if (i == 10):
                got10 = True
            
        self.assertTrue(got5)
        self.assertFalse(got10)

        ran = 0
        for i in range(6,6):
            ran = ran +1
        self.assertEqual(ran,0)

        zero = False
        twentythree = False
        twentyfour = False
        for i in range(24):
            if i == 0:
                zero = True
            if i == 23:
                twentythree = True
            if i == 24:
                twentyfour = True
        self.assertTrue(zero)
        self.assertTrue(twentythree)
        self.assertFalse(twentyfour)

        hasRun = False
        for i in range(5,5):
            hasRun = True
        self.assertFalse(hasRun)

    def testListCreation(self):
        a = 5
        b = [a]
        self.assertTrue(isinstance(b,list))

    def testListWrapping(self):
        liste = [1,2,3,4,5]

        self.assertEqual(liste[-1], 5)
        self.assertEqual(liste[-2], 4)

    def testIntAsBool(self):
        self.assertFalse(0)
        self.assertTrue(15)
        self.assertTrue(1)

    def testMod(self):
        self.assertTrue( (5 % 2) == 1)
        self.assertTrue( (102 % 2) == 0)
        
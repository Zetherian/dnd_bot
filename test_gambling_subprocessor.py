import unittest
import gambling_subprocessor as gambler


#Simple test suite for the basic math done in the gambler.
#Todo:
#   Update tests to do more than validate random inputs, tests should validate mathmatical truths as well
#   Add more functions once rounding gets settled.



#Constants
ALL_DICE=[1, #Because people will try it
          2,
          3, #There are rock/paper/scissor dice.
          4,
          6,
          8,
          10, #Handles d10 and perc
          12,
          20]

ROLL_AMT=[1,
          2,
          4,
          16,
          256]


class TestSimple(unittest.TestCase):

    #Tests for simple_math
    #Really too simple of a function to test but nonetheless tested to be thorough.

    def test_len(self):
       #Ensures the size of the results matches the nunmber of dice rolled
        for amount in ROLL_AMT:
            for dice in ALL_DICE:
                result=len(gambler.simple_math(amount, dice))
                self.assertEqual(amount, result)

        #Testing for times > 1 without a dice val.
        with self.assertRaises(ValueError) as ve:
           len(gambler.simple_math(1,0))

        #Validating we can roll a dice zero times
        none = len(gambler.simple_math(0, ALL_DICE[-1]))
        self.assertEqual(none, 0)


    def test_neg(self):
        #We're doing negative tests even though regex should trim them.
        #just to validate what should happen
        n_times=gambler.simple_math(-1, 20)         #I feel like these two assertions, should raise exceptions.
        double_n=gambler.simple_math(-200, -200)    #Considering it is not possible to have negative dicerolls with no modifiers.

        self.assertEqual(double_n, [])
        self.assertEqual(n_times, [])

        with self.assertRaises(ValueError) as ve:
            gambler.simple_math(9999, -20)


    def test_val(self):
        #Make sure all the rolled values are under the dice's maximum
        for dice in ALL_DICE:
            result=gambler.simple_math(ROLL_AMT[-1], dice)
            for value in result:
                self.assertLessEqual(value, dice)





class TestComplex(unittest.TestCase):

    #Lots of tests for complex.
    #So assuming the previous tests pass, negative tests only have to be done on the operand


    #Testing positive/negative , single/multi valued lists where we can.
    #We can add more complex tests as the need arises.
    def test_add(self):
        exp="+"

        simple=gambler.complex_math([10], exp, 5)
        n_simple=gambler.complex_math([10], exp, -5)

        multi=gambler.complex_math([20, 15, 10, 5, 1], exp, 10)
        n_multi=gambler.complex_math([20, 15, 10, 5, 1], exp, -10)

        self.assertEqual(simple, [15])
        self.assertEqual(n_simple, [5])

        self.assertEqual(multi, [30, 25, 20, 15, 11])
        self.assertEqual(n_multi, [10, 5, 0, -5, -9])


    def test_sub(self):
        exp="-"

        simple=gambler.complex_math([10], exp, 5)
        n_simple=gambler.complex_math([10], exp, -5)

        multi=gambler.complex_math([20, 15, 10, 5, 1], exp, 10)
        n_multi=gambler.complex_math([20, 15, 10, 5, 1], exp, -10)

        self.assertEqual(simple, [5])
        self.assertEqual(n_simple, [15])

        self.assertEqual(multi, [10, 5, 0, -5, -9])
        self.assertEqual(n_multi, [30, 25, 20, 15, 11])

    def test_mul(self):
        exp="*"

        simple=gambler.complex_math([10], exp, 5)
        n_simple=gambler.complex_math([10], exp, -5)

        multi=gambler.complex_math([20, 15, 10, 5, 1], exp, 10)
        n_multi=gambler.complex_math([20, 15, 10, 5, 1], exp, -10)

        self.assertEqual(simple, [50])
        self.assertEqual(n_simple, [-50])

        self.assertEqual(multi, [200, 150, 100, 50, 10])
        self.assertEqual(n_multi, [-200, -150, -100, -50, -10])


    #Tests below this point suffer in what they can do at the current rounding state.
    #They should be treated as placeholders and not trusted.
    def test_div(self):
        #This does not account for proper divison as the plan is to use floor div to fix rounding errors.
        exp="/"

        simple=gambler.complex_math([10], exp, 5)
        n_simple=gambler.complex_math([10], exp, -5)

        multi=gambler.complex_math([20, 15, 10, 5, 1], exp, 10)
        n_multi=gambler.complex_math([20, 15, 10, 5, 1], exp, -10)

        self.assertEqual(simple, [2])
        self.assertEqual(n_simple, [-2])

        #self.assertEqual(multi, [2, 1, 1, 0, 0])       These tests are being excluded until rounding gets figured out.
        #self.assertEqual(n_multi, [-2, -2, -1, -1, -1])

    def test_pow(self):
        #This does not account for proper divison as the plan is to use floor div to fix rounding errors.
        exp="^"

        simple=gambler.complex_math([10], exp, 5)
        n_simple=gambler.complex_math([10], exp, -5)

        multi=gambler.complex_math([10, 8, 5, 3, 1], exp, 10)
        n_multi=gambler.complex_math([20, 15, 10, 5, 1], exp, -10)

        self.assertEqual(simple, [100000])
        #self.assertEqual(n_simple, [0]) Being left out until rounding gets figured out

    def test_mod(self):
        exp="%"

        simple=gambler.complex_math([10], exp, 5)
        n_simple=gambler.complex_math([10], exp, -5)

        multi=gambler.complex_math([45, 37, 20, 11, 0], exp, 10)
        n_multi=gambler.complex_math([45, 37, 20, 11, 0], exp, -10)

        self.assertEqual(simple, [0])
        self.assertEqual(n_simple, [0])

        self.assertEqual(multi, [5, 7, 0, 1, 0])
        self.assertEqual(n_multi, [-5, -3, 0, -9, 0])



if __name__ == '__main__':
    unittest.main()

__author__ = 'Elad Sofer <eladsofe@post.bgu.ac.il>'

from argparse import ArgumentParser

OPTIONS = ('pi', 'fibonacci', 'prime')


class CSEx1Tool(object):
    """
    CS Ex1 Tool class
    """
    def __init__(self, task, n_param):
        self.task = task
        self.n_param = n_param
        # each counter starts from a different number
        self.PI_COUNTER = 0
        self.FIB_COUNTER = 1
        self.PRIME_COUNTER = 2

    def start(self):
        """
        Main function which starts the tool. the function redirects a task
        to it's corresponding function via searching the object's __dict__
        all the tasks' functions follows the standard of "task_name"_calc
        the tasks options are defined in OPTIONS var
        :return: the task's result
        """
        try:
            return getattr(self, '{task}_calc'.format(task=self.task))()
        except Exception:
            print ("an exception occurred during calculation...")
            raise

    def prime_calc(self):
        """
        A function which calculates the Nth prime number. the function verifies
        if a number is prime or not by caching all prime numbers before that
        specific number.
        The function is designated for maximum efficiency with cache array
        and +2 jumps between each number untill the number's sqrt
        :return the Nth prime number

        """
        curr_num = 3
        prime_numbers_cache = [2, 3]
        # if the user asked for N=1,2, the function returns it immediately
        if self.n_param <= 2:
            return prime_numbers_cache[self.n_param - 1]

        while self.PRIME_COUNTER != self.n_param:
            is_prime = True
            curr_num += 2
            for p in prime_numbers_cache:
                if curr_num % p == 0:
                    is_prime = False
                    break
                # If p is greater the sqrt of the curr_num, there is no way that
                # curr_num will have a future factor.
                elif p>curr_num**0.5:
                    break

            if is_prime:
                self.PRIME_COUNTER += 1
                prime_numbers_cache.append(curr_num)

        return curr_num

    def fibonacci_calc(self, first=0, second=1):
        """
        from Wiki -
        a series of numbers in which each number ( Fibonacci number )
         is the sum of the two preceding numbers. The simplest is the series
         1, 1, 2, 3, 5, 8, etc. *start counting from 1*

        A function which calculates the Nth fibonacci number by iterations
        :param first: which number to start from in the fibonacci calc
        :param second: the second number to start from in the fibonacci calc
        :return: the Nth fibonacci number
        """
        # in case N=1 init aN
        an = first+second

        while self.FIB_COUNTER != self.n_param:
            self.FIB_COUNTER += 1
            an = first + second
            first = second
            second = an

        return an

    @staticmethod
    def string_manipulation(src_string):
        """
        A function which receive a string as param and return the same string
        with a new row between each 40 chars.
        :param src_string: the source string
        :return: the string after the 40 digits manipulation
        """
        if len(src_string) <= 40:
            return src_string

        dest_string =  ''.join(['{0}{1}'.format(ch, '\n') if (ch_index + 1) % 40 == 0
                        else ch for ch_index, ch in enumerate(src_string)])

        # if the string length is exactly divided by 40.. so the last \n is
        # no needed
        if len(src_string)%40==0:
            return dest_string[:-1]

        return dest_string

    def sqrt(self, n, one):
        """
        Return the square root of n as a fixed point number with the one
        passed in.  It uses a second order Newton-Raphson convgence.  This
        doubles the number of significant figures on each iteration.
        """
        # Use floating point arithmetic to make an initial guess
        point_percision = 10 ** 16
        n_float = float(
            (n * point_percision) // one) / point_percision
        x = (int(
            point_percision * n_float ** 0.5) * one) // point_percision
        n_one = n * one
        while 1:
            x_old = x
            x = (x + n_one // x) // 2
            if x == x_old:
                break
        return x

    def pi_calc(self):
        """
        --------Stack Over flow--------
        Calculate pi using Chudnovsky's series
        return: the function returns pi until the Nth figure

        """
        ADDITIONAL_PERCISION = 50
        one = 10 ** (self.n_param + ADDITIONAL_PERCISION)
        k = 1
        a_k = one
        a_sum = one
        b_sum = 0
        C = 640320
        C3_OVER_24 = C ** 3 // 24
        while 1:
            a_k *= -(6 * k - 5) * (2 * k - 1) * (6 * k - 1)
            a_k //= k * k * k * C3_OVER_24
            a_sum += a_k
            b_sum += k * a_k
            k += 1
            if a_k == 0:
                break
        total = 13591409 * a_sum + 545140134 * b_sum
        pi = (426880 * self.sqrt(10005 * one, one) * one) // total

        # string manipulations for converting to the task format...
        pi_string = str(pi)[:self.n_param + 1]
        pi_string = '{0}.{1}'.format(pi_string[:1], pi_string[1:])

        return pi_string


if __name__ == '__main__':
    # Argument parsing - set default for "wrong input" value in order
    # to force the user to enter the arguments.
    parser = ArgumentParser("Introduction to CS - EX1 Tool - Elad Sofer")
    parser.add_argument('--task', action='store', dest='task', type=str,
                        default='NO_TASK_WAS_ENTERED',
                        help='choose which task to perform')
    parser.add_argument('--N', action='store', type=int, default=0,
                        help='The N parameter for each task')
    args = parser.parse_args()

    # Input validation process - P.S the parser handles arg "type exceptions"
    # The task require to print "wrong input" only for wrong N size,
    #  or undefined task
    if args.task in OPTIONS and 0 < args.N <= 1000:
        tool = CSEx1Tool(args.task, args.N)
        result = tool.start()
        result = tool.string_manipulation(str(result))
        print (result)
    else:
        print ("wrong input")

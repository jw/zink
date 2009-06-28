class Chain(object):
    """
    Chains together several iterables into a single subscriptable iterable.
    
    It is different to ``itertools.chain`` in that it is subscriptable.  It
    assumes that the lengths of the composing iterables do not change during its
    lifetime.

    It also implements the functions ``count`` and ``filter`` so it can
    half-heartedly pretend it's a django query.

    >>> my_chain = Chain([0, 1, 2], ['blue', 'green'], [4, 7, 8])
    >>> for item in my_chain:
    ...     print item,
    0 1 2 blue green 4 7 8
    >>> my_chain[4]
    'green'
    >>> my_chain.count()
    8
    >>> len(my_chain)
    8
    """

    def __unicode__(self):
        return unicode(list(self))

    def __init__(self,*iterables):
        self.iterables = iterables
        self.lengths = None

    def _set_lengths(self):
        self.lengths = []
        for iterable in self.iterables:
            self.lengths.append(len(iterable))

    def __getitem__(self,k):
        if self.lengths is None:
            self._set_lengths()
        total_length = 0
        for iterable, length in zip(self.iterables, self.lengths):
            if k < total_length + length:
                return iterable[k-total_length]
            total_length += length
        raise IndexError

    def count(self):
        return len(self)

    class Iterator(object):
        def __init__(self, iterables):
            self.iterator_of_iterables = iterables.__iter__()
            self.iterator_of_objects = self.iterator_of_iterables.next().__iter__()
        def next(self):
            while True:
                try:
                    object = self.iterator_of_objects.next()
                    return object
                except StopIteration:
                    # We let a StopIteration from this one bubble up
                    self.iterator_of_objects = self.iterator_of_iterables.next().__iter__()

    def __iter__(self):
        return self.Iterator(self.iterables)

    def __len__(self):
        if self.lengths is None:
            self._set_lengths()
        total_length = 0
        for length in self.lengths:
            total_length += length
        return total_length

    def filter(self,*args,**kwargs):
        new_iterables= []
        for iterable in self.iterables:
            new_iterable = iterable.filter(*args,**kwargs)
            new_iterables.append(new_iterable)
        return Chain(new_iterables)

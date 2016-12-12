/**
 * Created by Matthew Crocco on 12/11/2016.
 */

/// <reference path='./libs/lodash.d.ts' />

const existential = (() => {

    class Nothing<T> {}
    class Just<T> { value: T; }
    type Maybe<T> = Nothing<T> | Just<T>

    function make<T>(value?: T): Maybe<T> {
        return _.isNil(value) ? {} : {value: value};
    }

    function isNothing<T>(maybe: Maybe<T>): maybe is Nothing<T> {
        return maybe instanceof Nothing;
    }

    function isJust<T>(maybe: Maybe<T>): maybe is Just<T> {
        return maybe instanceof Just;
    }

    function maybe<T>(optional: Maybe<T>, def: T): T {
        return isJust<T>(optional) ? optional.value : def;
    }

    function fromJust<T>(optional: Maybe<T>): T {
        if (isNothing<T>(optional))
            throw new TypeError(`${typeof(optional)} is not a Just type.`);
        else
            return (<Just<T>>optional).value;
    }

    function catMaybes<T>(...maybes: Maybe<T>[]): T[] {
        const result: T[] = [];

        for (const maybe of maybes)
            if (isJust<T>(maybe))
                result.push((<Just<T>>maybe).value);

        return result;
    }


    function mapMaybes<T, U>(transform: (x: T) => U, ...maybes: Maybe<T>[]) {
        const result: U[] = [];

        for (const value of catMaybes<T>(...maybes))
            result.push(transform(value));

        return result;
    }
    
    make.prototype = _.assign(make.prototype, {
        Nothing,
        Just,
        make,
        isNothing,
        isJust,
        maybe,
        fromMaybe: maybe,
        fromJust,
        catMaybes,
        mapMaybes
    });
    
    return make;
})();

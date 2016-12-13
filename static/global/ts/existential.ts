/**
 * Created by Matthew Crocco on 12/11/2016.
 */

import * as _ from 'lodash';

interface Maybe<T> {
    get(def?: T): T;
    exists(): boolean;
}

class Nothing<T> implements Maybe<T> {
    get(def?: T): T {
        if (_.isNil(def))
            throw new ReferenceError("Value is Nothing");
        return def;
    }
    
    exists(): boolean {
        return false;
    }
}

class Just<T> implements Maybe<T> {
    value: T;
    
    constructor(value: T) {
        this.value = value;
    }
    
    get(def?: T): T {
        return this.value;
    }
    
    exists(): boolean {
        return true;
    }
}

function make<T>(value?: T): Maybe<T> {
    return _.isNil(value) ? new Nothing<T>() : new Just(value);
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

function existRoot<T>(x?: T | Maybe<T>, def?: T) {
    if(_.isNil(x) || !(x instanceof Just || x instanceof Nothing)) {
        return make(<T>x);
    } else
        return maybe(<Maybe<T>>x, def);
}

existRoot.prototype = _.assign(existRoot.prototype, {
    Nothing,
    Just,
    make,
    isNothing,
    isJust,
    maybe,
    fromJust,
    catMaybes,
    mapMaybes
});

export {
    Nothing,
    Just,
    Maybe,
    make,
    isNothing,
    isJust,
    maybe,
    fromJust,
    catMaybes,
    mapMaybes
};

const Existential = existRoot;

export default Existential;


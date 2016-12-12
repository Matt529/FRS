/**
 * Created by Matthew Crocco on 12/11/2016.
 */

import * as _ from 'lodash';

export namespace Existentials {
    export class Nothing<T> {}
    export class Just<T> { value: T; }
    type Maybe<T> = Nothing<T> | Just<T>

    export function make<T>(value?: T): Maybe<T> {
        return _.isNil(value) ? {} : {value: value};
    }

    export function isNothing<T>(maybe: Maybe<T>): maybe is Nothing<T> {
        return maybe instanceof Nothing;
    }

    export function isJust<T>(maybe: Maybe<T>): maybe is Just<T> {
        return maybe instanceof Just;
    }

    export function maybe<T>(optional: Maybe<T>, def: T): T {
        return isJust<T>(optional) ? optional.value : def;
    }

    export function fromJust<T>(optional: Maybe<T>): T {
        if (isNothing<T>(optional))
            throw new TypeError(`${typeof(optional)} is not a Just type.`);
        else
            return (<Just<T>>optional).value;
    }

    export function catMaybes<T>(...maybes: Maybe<T>[]): T[] {
        const result: T[] = [];

        for (const maybe of maybes)
            if (isJust<T>(maybe))
                result.push((<Just<T>>maybe).value);

        return result;
    }


    export function mapMaybes<T, U>(transform: (x: T) => U, ...maybes: Maybe<T>[]) {
        const result: U[] = [];

        for (const value of catMaybes<T>(...maybes))
            result.push(transform(value));

        return result;
    }
}

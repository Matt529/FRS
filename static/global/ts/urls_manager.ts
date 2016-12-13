/**
 * Created by Matthew Crocco on 12/12/2016.
 */

import Existential from './existential';
import {Maybe} from './existential';

declare const Urls: Object;

interface UrlHandle {
    name(): string;
    params(): string[];
    paramCount(): number;
    
    createUrl(...args: any[]): string;
    goto(...args: any[]): void;
}

type UrlFn = (...args: any[]) => string;
class GotoUrlHandle implements UrlHandle {
    urlName: string;
    urlFunc: UrlFn;
    
    constructor(name: string, urlFunc: UrlFn) {
        this.urlName = name;
        this.urlFunc = urlFunc;
    }
    
    name(): string {
        return this.urlName;
    }
    
    params(): string[] {    // TODO Replace django-reverse-js
        throw new Error("Not Implemented Yet");
    }
    
    paramCount(): number {  // TODO Replace django-reverse-js
        return null;
    }
    
    createUrl(...args: any[]): string {
        return this.urlFunc(...args);
    }
    
    goto(...args): void {
        window.location.replace(this.createUrl(...args));
    }
}


function getUrlByName(djangoName: string): Maybe<UrlHandle> {
    if(Urls.hasOwnProperty(djangoName)) {
        return <Maybe<UrlHandle>>Existential(new GotoUrlHandle(djangoName, <UrlFn>Urls[djangoName]));
    } else
        return <Maybe<UrlHandle>>Existential();
}

const UrlProvider = {
    getUrlByName
};

export default UrlProvider;
export {
    getUrlByName
};

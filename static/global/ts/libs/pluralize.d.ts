/**
 * Created by Matthew Crocco on 12/11/2016.
 */
// Type definitions for pluralize
// Project: https://www.npmjs.com/package/pluralize
// Definitions by: Syu Kato <https://github.com/ukyo>
// Definitions: https://github.com/DefinitelyTyped/DefinitelyTyped

interface PluralizeStatic {
    /**
     * Pluralize or singularize a word based on the passed in count.
     *
     * @param word
     * @param count
     * @param inclusive
     */
    (word: string, count?: number, inclusive?: boolean): string;

    /**
     * Pluralize a word based.
     *
     * @param word
     */
    plural(word: string): string;

    /**
     * Singularize a word based.
     *
     * @param word
     */
    singular(word: string): string;

    /**
     * Add a pluralization rule to the collection.
     *
     * @param rule
     * @param replacement
     */
    addPluralRule(rule: string|RegExp, replacemant: string): void;

    /**
     * Add a singularization rule to the collection.
     *
     * @param rule
     * @param replacement
     */
    addSingularRule(rule: string|RegExp, replacemant: string): void;

    /**
     * Add an irregular word definition.
     *
     * @param single
     * @param plural
     */
    addIrregularRule(single: string, plural: string): void;

    /**
     * Add an uncountable word rule.
     *
     * @param word
     */
    addUncountableRule(word: string|RegExp): void;
}

declare const pluralize: PluralizeStatic;

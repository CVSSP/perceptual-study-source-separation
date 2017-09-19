function fromAToBArray(a, b)
{
    if (b <= a)
        b = a + 1;

    var n = b - a;
    var array = new Array(n);
    for (var i = 0; i < n; ++i)
        array[i] = a + i;

    return array;
}

function arrayFilledWith(value, size)
{
    var array = new Array(size);
    for (var i = 0; i < size; ++i)
        array[i] = value;
    return array;
}

function randomNumber(min, max, shouldRound)
{
    var val = Math.random();
    var range = max - min;
    val *= range;
    val += min;

    if (shouldRound)
        val = Math.floor (val)
    return val;
}

/**
 * Shuffles array in place.
 * @param {Array} a items The array containing the items.
 * From: https://stackoverflow.com/questions/6274339/how-can-i-shuffle-an-array
 */
function shuffle(a) {
    var j, x, i;
    for (i = a.length; i; i--) {
        j = Math.floor(Math.random() * i);
        x = a[i - 1];
        a[i - 1] = a[j];
        a[j] = x;
    }
}

function selectMaximum (a, b)
{
    if (a > b)
        return a;
    else
        return b;
}

function selectMinimum (a, b)
{
    if (a < b)
        return a;
    else
        return b;
}

function newSortedArray (array)
{
    newArray = array.slice();
    return newArray.sort (function (a, b) {return a - b;});
}

function indicesNeededToSortArray (array)
{
    newArray = fromAToBArray (0, array.length);
    return newArray.sort (function (a, b) { return array[a] < array[b] ? -1 : array[a] > array[b] ? 1 : 0; });
}




/** JQM **/
/* Wrapper for selecting elements on active page:
https://forum.jquery.com/topic/usage-of-ids-impossible
*/
function $activePage(query='') {return $('.ui-page-active ' + query);}


// https://stackoverflow.com/questions/10716986/swap-2-html-elements-and-preserve-event-listeners-on-them
function swapElements(obj1, obj2) {

    // create marker element and insert it where obj1 is
    var temp = document.createElement("div");
    obj1.parentNode.insertBefore(temp, obj1);

    // move obj1 to right before obj2
    obj2.parentNode.insertBefore(obj1, obj2);

    // move obj2 to right before where obj1 used to be
    temp.parentNode.insertBefore(obj2, temp);

    // remove temporary marker node
    temp.parentNode.removeChild(temp);
}

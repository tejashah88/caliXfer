# Path parameters of assist.org urls
* `ia` - id of origin school
* `oia` - id of destination school
* `ay` - articulation year range
* `aay`* - seems to be the same as `ay`
* `inst1`* - unknown (probably used somewhere else)
* `inst2`* - unknown (probably used somewhere else)
* `dora` - id of selected major or `GE`
* `agreement` - agreement type
  * `aa` - articulation agreement
  * `tca` - CSU/UC specific agreements
* `event` - internal event id
  * `18` - by department
  * `19` - by major
  * `21` - for GE/breadth
  * `23` - 'CSU transferable courses' - by department
  * `24` - 'CSU GE-Breadth Certification Courses' - by breadth area
  * `25` - 'CSU GE-Breadth Certification Courses' - by department
  * `26` - 'IGETC for UC and CSU' - by department
  * `27` - 'IGETC for UC and CSU' - by IGETC area
  * `28` - 'UC Transferable Courses' - by department
  * `29` - 'UC Transfer Admission Eligibility Courses' - by eligibility area
  * `30` - 'CSU US History, Constitution, and American Ideals Courses'
* `dir` - used to signify if the origin and destination schools are swapped
  * `1` - not swapped
  * `2` - swapped
  * **explanation**: When selecting from the 'Agreements with Other Campuses', some options will have 'From: ....'. What this means is that selecting a 'from' school will set it as the origin school and the previously selected school as the destination. Selecting the reverse order with a 'To: ....' school will yield the same exact effects.
* `swap` - similar to `dir` but for indicating if the selected department was from the origin school or destination school.
  * `0` - department comes from origin school
  * `1` - department comes from destination school
* `dt` - seems to determine the formatting of the articulation report
  * `0` - PDF format
  * `2` - text-only format
* `rinst` - determines which side the destination school courses will be (either 'right' or 'left')

\* needs more info
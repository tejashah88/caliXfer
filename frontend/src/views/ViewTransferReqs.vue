<template>
  <div>
    <h1>View Transfer Requirements</h1>
    <FuzzyAutoComplete
      label="This is a label"
      placeholder="This is a placeholder"
      item-text="Description"
      item-value="API"
    ></FuzzyAutoComplete>
  </div>
</template>

<script>

import FuzzyAutoComplete from '@/components/FuzzyAutoComplete';

export default {
  name: 'ViewTransferReqs',
  components: {
    FuzzyAutoComplete
  }
};
</script>
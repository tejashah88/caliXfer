<template>
  <div>
    <h1>Explore Universities</h1>
    <outdated-agreement-warning/>
  </div>
</template>

<script>
// import FuzzyAutoComplete from '@/components/FuzzyAutoComplete';
import OutdatedAgreementWarning from '@/components/OutdatedAgreementWarning';
import MemoizedAssistAPI from '@/pseudo-assist-api.js';

export default {
  name: 'ExploreUnis',
  components: {
    // FuzzyAutoComplete,
    OutdatedAgreementWarning
  },
};
</script>
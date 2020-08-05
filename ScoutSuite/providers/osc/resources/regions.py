import abc

from ScoutSuite.providers.osc.resources.base import OSCCompositeResources
from ScoutSuite.providers.osc.facade.base import OSCFacade


class Regions(OSCCompositeResources, metaclass=abc.ABCMeta):

    def __init__(self, service: str, facade: OSCFacade):
        super(Regions, self).__init__(facade)
        self.service = service

    async def fetch_all(self, regions=None, excluded_regions=None, **kwargs):
        import logging
        logging.getLogger("scout").critical("OSC ::: Regions::fetch_all()")
        self['regions'] = {}
        for region in await self.facade.build_region_list(self.service, regions, excluded_regions):
            self['regions'][region['RegionName']] = {
                'id': region,
                'region': region,
                'name': region
            }

        await self._fetch_children_of_all_resources(
            resources=self['regions'],
            scopes={region: {'region': region} for region in self['regions']}
        )
        self._set_counts()

    def _set_counts(self):
        self['regions_count'] = len(self['regions'])

        for _, key in self._children:
            if key == 'vpcs':
                continue

            self[key + '_count'] = sum([region[key + '_count'] for region in self['regions'].values()])
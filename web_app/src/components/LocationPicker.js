import { useMapEvents } from "react-leaflet";
import { useSelector } from "react-redux";
import { toast } from 'react-toastify';
import {DADATA_TOKEN, GET_MAP_CENTER} from "../const";
import {useTaxiActions, useUIActions} from "../store/useActions";
import {useEffect} from "react";
import axios from "axios";
import {useUISelector} from "../store/useSelectors";
import {nominatimReverse} from "../api/nominatim";
import {nominatimProcessResult} from "../services/nominatim";


export const LocationPicker = (props) => {
  const { pickLocationField } = useUISelector();
  const { setCenterPosition } = useUIActions();
  const { setStartAddress, setEndAddress, setStartLocation, setEndLocation,  } =
    useTaxiActions();

  useEffect(() => {
      axios.get(GET_MAP_CENTER)
            .then(response => {
                var payload = response.data
                if (!payload) return;
                var coords = payload.web_app_map_center.coordinates
                setCenterPosition(coords.reverse())
            })
            .catch(error => {
                console.error(error)
            })
  }, [])

  const mapEvents = useMapEvents({
    click(event) {
      if (!pickLocationField) return;

      const coords = event.latlng;
      try {

        nominatimReverse(coords.lat, coords.lng)
          .then((response) => response.data)
          .then((resultJson) => {
            if (!resultJson) return;
            const result = nominatimProcessResult(resultJson);
            if (pickLocationField === "start") {
              setStartAddress(result.set_name);
              setStartLocation({
                latitude: parseFloat(coords.lat),
                longitude: parseFloat(coords.lng),
              });
            } else {
              setEndAddress(result.set_name);
              setEndLocation({
                latitude: parseFloat(coords.lat),
                longitude: parseFloat(coords.lng),
              });
            }
          }).catch(error => toast.error("Не удалось определить адрес"));
        } catch {
            toast.error("Не удалось определить адрес")
        }
    },
  });

  return null;
};
